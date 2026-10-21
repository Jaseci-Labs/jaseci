// Diagnostic contracts: host proves single Scalar seeds, degree <=1,
// bounded int64 products/sums and matching length K before these kernels run.
// These are not replacements for the general checked Jac walker.
#include <stdint.h>
using I = int64_t;

extern "C" __global__ void graph_chain_csr(
    const I* values, const I* offsets, const I* targets, const I* heads,
    I* output, unsigned* status, I nodes, I lanes) {
    I lane = (I)blockIdx.x * blockDim.x + threadIdx.x;
    if (lane >= lanes) return;
    I a = heads[lane], b = heads[lanes + lane], sum = 0;
    while (a >= 0 && b >= 0) {
        sum += values[a] * values[b];
        I ab = offsets[a], ae = offsets[a + 1];
        I bb = offsets[nodes + 1 + b], be = offsets[nodes + 2 + b];
        a = ab < ae ? targets[ab] : -1;
        b = bb < be ? targets[bb] : -1;
    }
    output[lane] = sum;
    status[lane] = 0;
}

extern "C" __global__ void graph_chain_next(
    const I* values, const I* next, const I* heads,
    I* output, unsigned* status, I nodes, I lanes) {
    I lane = (I)blockIdx.x * blockDim.x + threadIdx.x;
    if (lane >= lanes) return;
    I a = heads[lane], b = heads[lanes + lane], sum = 0;
    while (a >= 0 && b >= 0) {
        sum += values[a] * values[b];
        a = next[a];
        b = next[nodes + b];
    }
    output[lane] = sum;
    status[lane] = 0;
}

extern "C" __global__ void graph_schedule(
    const I* values, const I* a_indices, const I* b_indices,
    I* output, unsigned* status, int M, int K, int N) {
    I lane = (I)blockIdx.x * blockDim.x + threadIdx.x;
    if (lane >= (I)M * N) return;
    int i = lane / N, j = lane % N;
    I sum = 0;
    #pragma unroll 1
    for (int q = 0; q < K; ++q)
        sum += values[a_indices[(I)q*M+i]] * values[b_indices[(I)q*N+j]];
    output[lane] = sum;
    status[lane] = 0;
}

// Match the graph arms' one-dimensional 128-thread geometry and lane order.
extern "C" __global__ void matmul_flat_i64(
    const I* A, const I* B, I* C, int M, int K, int N) {
    I lane = (I)blockIdx.x * blockDim.x + threadIdx.x;
    if (lane >= (I)M * N) return;
    int i = lane / N, j = lane % N;
    I sum = 0;
    #pragma unroll 1
    for (int q = 0; q < K; ++q) sum += A[(I)i*K+q] * B[(I)q*N+j];
    C[lane] = sum;
}
