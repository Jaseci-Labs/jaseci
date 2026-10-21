// Dense int64 baselines for Jac's named-cursor Dot example.
// Inputs are row-major A[M,K], B[K,N]; each thread owns one C element.
// The benchmark bounds every product and sum inside signed int64.
#include <stdint.h>

extern "C" __global__ void matmul_naive_i64(
    const int64_t* A, const int64_t* B, int64_t* C, int M, int K, int N) {
    int j = blockIdx.x * blockDim.x + threadIdx.x;
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    if (i >= M || j >= N) return;
    int64_t sum = 0;
    for (int k = 0; k < K; ++k)
        sum += A[(int64_t)i*K+k] * B[(int64_t)k*N+j];
    C[(int64_t)i*N+j] = sum;
}

// A block computes a 16x16 C tile. The 256 threads cooperatively load
// 256 A and B values per K tile; each value is reused by 16 threads.
// Out-of-bounds lanes load zero and still participate in both barriers.
extern "C" __global__ void matmul_tiled_i64(
    const int64_t* A, const int64_t* B, int64_t* C, int M, int K, int N) {
    constexpr int T = 16;
    __shared__ int64_t a[T][T];
    __shared__ int64_t b[T][T];
    int x = threadIdx.x, y = threadIdx.y;
    int i = blockIdx.y*T+y, j = blockIdx.x*T+x;
    int64_t sum = 0;
    for (int base = 0; base < K; base += T) {
        a[y][x] = (i < M && base+x < K) ? A[(int64_t)i*K+base+x] : 0;
        b[y][x] = (base+y < K && j < N) ? B[(int64_t)(base+y)*N+j] : 0;
        __syncthreads();
        #pragma unroll
        for (int k = 0; k < T; ++k) sum += a[y][k] * b[k][x];
        __syncthreads();
    }
    if (i < M && j < N) C[(int64_t)i*N+j] = sum;
}
