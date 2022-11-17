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
	const size_t* starts, const size_t starts_size,
	const size_t length,
	const float ray_slope)
{
	float visible = starts_size;
	float condition = starts_size;

	for(size_t m=0; m<starts_size; m++){
		const size_t start = starts[m];

		if (height[start+1] - height[start] > ray_slope){
			condition -= 1;
			visible -= 1;
			continue;
		}

		for(size_t i=0; i<length; i++){
			if(height[start] + ray_slope*i < height[start + i]){
				visible -= 1;
				break;
			}
		}
	}
	return visible / condition;
}


}