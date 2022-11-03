#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;


#include <cmath>
#include <numbers>


PYBIND11_MODULE(distributions, m) {
	{
		auto _m = m.def_submodule("ggx");

		_m.def("name", [](){return "ggx";});

		_m.def("ndf", py::vectorize([](float th_m, float alpha){
			float a2 = alpha*alpha;
			float sin = std::sin(th_m);
			float cos = std::cos(th_m);
			float kakko = sin*sin/a2 + cos*cos;
			return 1/(std::numbers::pi * a2 * kakko*kakko);
		}));

		_m.def("smith_g1", py::vectorize([](float th_v, float alpha){
			float alpha_tan = alpha * std::tan(th_v);
			return 2/(1 + std::sqrt(1 + alpha_tan*alpha_tan));
		}));
	}

	{
		auto _m = m.def_submodule("beckmann");

		_m.def("name", [](){return "beckmann";});

		_m.def("ndf", py::vectorize([](float th_m, float alpha){
			float a2 = alpha*alpha;
			float sin = std::sin(th_m);
			float cos = std::cos(th_m);

			float sin2 = sin*sin;
			float cos2 = cos*cos;

			return std::exp(-sin2/cos2/a2) / (std::numbers::pi * a2 * cos2*cos2);
		}));

		_m.def("smith_g1", py::vectorize([](float th_v, float alpha){
			float a = 1/(alpha*std::tan(th_v));
			return 2/(1 + std::erf(a) +  std::exp(-a*a)/(a*std::sqrt(std::numbers::pi)));
		}));
	}
}
