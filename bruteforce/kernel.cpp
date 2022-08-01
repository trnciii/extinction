#include "kernel.hpp"

#include <cmath>
#include <numbers>


float ggx::ndf(float th_m, float alpha){
	float a2 = alpha*alpha;
	float sin = std::sin(th_m);
	float cos = std::cos(th_m);
	float kakko = sin*sin/a2 + cos*cos;
	return 1/(std::numbers::pi * a2 * kakko*kakko);
}

float ggx::smith_g1(float th_v, float alpha){
	float alpha_tan = alpha * std::tan(th_v);
	return 2/(1 + std::sqrt(1 + alpha_tan*alpha_tan));
}
