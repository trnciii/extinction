#include <cuda_runtime.h>
#include <iostream>
#include "kernel.cuh"

__global__ void visibility(float* visible,
	float* slope, size_t steps,
	float* height, size_t realizations, size_t length)
{
	size_t s = blockIdx.x*blockDim.x + threadIdx.x;
	if(s>=steps) return;

	visible[s] = realizations;
	for(size_t m=0; m<realizations; m++){
		for(size_t i=0; i<length; i++){
			if(height[m*length + 0] + slope[s]*i < height[m*length + i]){
				visible[s] -= 1;
				break;
			}
		}
	}

	visible[s] /= realizations;
}

void call_visibility(float* visible,
	float* slope, size_t steps,
	float* height, size_t realizations, size_t length)
{
	float* d_visible;
	cudaMallocManaged(&d_visible, steps*sizeof(float));

	float* d_slope;
	cudaMallocManaged(&d_slope, steps*sizeof(float));
	cudaMemcpy(d_slope, slope, steps*sizeof(float), cudaMemcpyDefault);

	float* d_height;
	cudaMallocManaged(&d_height, realizations*length*sizeof(float));
	cudaMemcpy(d_height, height, realizations*length*sizeof(float), cudaMemcpyDefault);

	int threads = 1024;
	visibility <<< steps/threads + 1, threads >>> (d_visible, d_slope, steps, d_height, realizations, length);
	cudaDeviceSynchronize();

	cudaMemcpy(visible, d_visible, steps*sizeof(float), cudaMemcpyDefault);

	cudaFree(d_visible);
	cudaFree(d_slope);
	cudaFree(d_height);
}