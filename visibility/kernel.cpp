#include "kernel.hpp"

void kernel(float* x, std::size_t n){
	for(int i=0; i<n; i++){
		x[i] += 10;
	}
}
