#include "kernel.h"

#include <cuda_runtime.h> 
#include "vector_math.h"


__global__ void kernel(float* x, uint32_t n){
	uint32_t i = blockIdx.x*blockDim.x + threadIdx.x;
	if(i>=n) return;
	x[i] += 10;
}


extern "C" void call_kernel(float* x, uint32_t n){
	for(int i=0; i<n; i++){
		std::cout <<x[i] <<", ";
	}
	std::cout <<std::endl;

	float* y;
	size_t size = n*sizeof(float);
	cudaMallocManaged(&y, size);
	cudaMemcpy(y, x, size, cudaMemcpyDefault);

	kernel <<<n/1024 + 1, 1024>>> (y, n);
	cudaDeviceSynchronize();

	cudaMemcpy(x, y, size, cudaMemcpyDefault);
	for(int i=0; i<n; i++){
		std::cout <<x[i] <<", "
;	}
	std::cout <<std::endl;
}
