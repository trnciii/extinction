#pragma once

#ifndef __CUDACC__
	#define __device__
#endif


namespace kernel{

__device__ float g1_distant(const float* height, size_t realizations, size_t length, float ray_slope){
	float visible = realizations;
	for(size_t m=0; m<realizations; m++){
		for(size_t i=0; i<length; i++){
			if( height[m*length] + ray_slope*i < height[m*length + i] ){
				visible -= 1;
				break;
			}
		}
	}

	return visible / realizations;
}

__device__ float g1_distant_single(
	const float* height,
	const size_t* starts, size_t starts_size,
	size_t length,
	float ray_slope)
{
	if(starts_size == 0) return 1;

	float visible = starts_size;
	for(size_t m=0; m<starts_size; m++){
		size_t start = starts[m];
		for(size_t i=0; i<length; i++){
			if(height[start] + ray_slope*i < height[start + i]){
				visible -= 1;
				break;
			}
		}
	}
	return visible / starts_size;
}


}