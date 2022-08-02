#include <cuda_runtime.h>

#include "kernel.cuh"

__global__ void visibility(float* x, size_t n){
	size_t i = blockIdx.x*blockDim.x + threadIdx.x;

	if(i>=n) return;

	x[i] += 10;
}

void call_visibility(float* x, size_t n){
	float* y;
	size_t size = n*sizeof(float);
	cudaMallocManaged(&y, size);
	cudaMemcpy(y, x, size, cudaMemcpyDefault);

	int threads = 1024;
	visibility <<<n/threads + 1, threads>>> (y, n);
	cudaDeviceSynchronize();

	cudaMemcpy(x, y, size, cudaMemcpyDefault);
	cudaFree(y);
}