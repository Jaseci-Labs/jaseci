// One thread per query, FIFO over the exact saved production CSR.
// Full checked primary path; bounded-input and queue-layout controls are supplementary.
#include <stdint.h>
#include <limits.h>
using I = int64_t;
using U = uint64_t;
#define PARAMETERS \
 const I* amount, const I* alert, const I* offsets, const I* targets, const I* heads, \
 const I* in_count, const I* in_total, const I* in_alert, const I* in_visited, const I* in_threshold, \
 I* out_count, I* out_total, I* out_alert, I* out_visited, I* out_threshold, \
 unsigned* status, I* queue, U nodes, U edges, U queries, U capacity, U max_visits
#define ARGUMENTS amount,alert,offsets,targets,heads,in_count,in_total,in_alert,in_visited,in_threshold, \
 out_count,out_total,out_alert,out_visited,out_threshold,status,queue,nodes,edges,queries,capacity,max_visits

__device__ __forceinline__ bool overflow_add(I a, I b) {
    return (b > 0 && a > INT64_MAX-b) || (b < 0 && a < INT64_MIN-b);
}

template<bool SlotMajor>
__device__ __forceinline__ U qi(U slot, U queries, U lane, U capacity) {
    return SlotMajor ? slot*queries+lane : lane*capacity+slot;
}

template<bool Overflow, bool Validate, bool SlotMajor>
__device__ __forceinline__ void subtree(PARAMETERS) {
    U lane = (U)blockIdx.x*blockDim.x+threadIdx.x;
    if (lane >= queries) return;
    I count = in_count[lane], total = in_total[lane], visited = in_visited[lane];
    I threshold = in_threshold[lane];
    bool has_alert = in_alert[lane] != 0;
    I root = heads[lane];
    if (root != -1) {
        if (Validate && capacity == 0) { status[lane] = 6; return; }
        U reader = 0, writer = capacity == 1 ? 0 : 1, pending = 1, steps = 0;
        queue[qi<SlotMajor>(0,queries,lane,capacity)] = root;
        while (pending) {
            I node = queue[qi<SlotMajor>(reader,queries,lane,capacity)];
            reader = reader+1 == capacity ? 0 : reader+1;
            --pending;
            if (Validate && (node < 0 || (U)node >= nodes)) { status[lane] = 1; return; }
            if (Validate && steps >= max_visits) { status[lane] = 2; return; }
            I value = amount[node];
            if (Overflow && visited == INT64_MAX) { status[lane] = 3; return; }
            ++visited;
            if (value >= threshold) {
                if (Overflow && (count == INT64_MAX || overflow_add(total, value))) { status[lane] = 3; return; }
                ++count;
                total += value;
                has_alert = has_alert || alert[node] != 0;
            }
            I begin = offsets[node], end = offsets[node+1];
            if (Validate && (begin < 0 || end < begin || (U)end > edges)) { status[lane] = 5; return; }
            U degree = (U)(end-begin);
            if (Validate && degree > capacity-pending) { status[lane] = 6; return; }
            for (I edge = begin; edge < end; ++edge) {
                I target = targets[edge];
                if (Validate && (target < 0 || (U)target >= nodes)) { status[lane] = 1; return; }
                queue[qi<SlotMajor>(writer,queries,lane,capacity)] = target;
                writer = writer+1 == capacity ? 0 : writer+1;
            }
            pending += degree;
            ++steps;
        }
    }
    out_count[lane] = count;
    out_total[lane] = total;
    out_alert[lane] = has_alert;
    out_visited[lane] = visited;
    out_threshold[lane] = threshold;
    status[lane] = 0;
}

extern "C" __global__ void subtree_checked(PARAMETERS) { subtree<true,true,true>(ARGUMENTS); }
extern "C" __global__ void subtree_unchecked(PARAMETERS) { subtree<false,false,true>(ARGUMENTS); }
extern "C" __global__ void subtree_query_major(PARAMETERS) { subtree<true,true,false>(ARGUMENTS); }
