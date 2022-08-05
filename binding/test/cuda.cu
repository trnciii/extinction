#include <cuda_runtime.h>
#include <iostream>
#include "cuda.cuh"

#include "kernel.hpp"


__global__ void visibility(float* visible,
	const float* ray_slope, size_t steps,
	const float* height, size_t realizations, size_t length)
{
	size_t s = blockIdx.x*blockDim.x + threadIdx.x;
	if(s>=steps) return;
	visible[s] = g1_distant(height, realizations, length, ray_slope[s]);
}

void call_visibility(float* visible,
	const float* ray_slope, size_t steps,
	const float* height, size_t realizations, size_t length)
{
	float* d_visible;
	cudaMallocManaged(&d_visible, steps*sizeof(float));

	float* d_ray_slope;
	cudaMallocManaged(&d_ray_slope, steps*sizeof(float));
	cudaMemcpy(d_ray_slope, ray_slope, steps*sizeof(float), cudaMemcpyDefault);

	float* d_height;
	cudaMallocManaged(&d_height, realizations*length*sizeof(float));
	cudaMemcpy(d_height, height, realizations*length*sizeof(float), cudaMemcpyDefault);

	int threads = 1024;
	visibility <<< steps/threads + 1, threads >>> (d_visible, d_ray_slope, steps, d_height, realizations, length);
	cudaDeviceSynchronize();

	cudaMemcpy(visible, d_visible, steps*sizeof(float), cudaMemcpyDefault);

	cudaFree(d_visible);
	cudaFree(d_ray_slope);
	cudaFree(d_height);
}