#pragma once

#include <cuda_runtime.h>

extern void call_visibility(float* visible,
	float* slope, size_t steps,
	float* height, size_t realizations, size_t length);
