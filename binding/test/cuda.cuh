#pragma once

#include <cuda_runtime.h>

extern void call_visibility(float* visible,
	const float* ray_slope, size_t steps,
	const float* height, size_t realizations, size_t length);
