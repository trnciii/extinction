#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;


#include <cmath>
#include <numbers>


PYBIND11_MODULE(ggx, m) {
	m.def("ndf", py::vectorize([](float th_m, float alpha){
		float a2 = alpha*alpha;
		float sin = std::sin(th_m);
		float cos = std::cos(th_m);
		float kakko = sin*sin/a2 + cos*cos;
		return 1/(std::numbers::pi * a2 * kakko*kakko);
	}));

	m.def("smith_g1", py::vectorize([](float th_v, float alpha){
		float alpha_tan = alpha * std::tan(th_v);
		return 2/(1 + std::sqrt(1 + alpha_tan*alpha_tan));
	}));

}
