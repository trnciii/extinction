#pragma once

#ifndef __CUDACC__
	#define __device__
#endif


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