#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

#include "cuda.cuh"

PYBIND11_MODULE(gpu, m){
	m.def("visibility", [](const py::array_t<float>& _height, const py::array_t<float>& _ray_slope){
		const auto height = _height.unchecked<2>();
		const auto ray_slope = _ray_slope.unchecked<1>();

		py::array_t<float> visible({ ray_slope.shape(0) });
		auto _vis = visible.mutable_unchecked<1>();

		call_visibility(_vis.mutable_data(0),
			ray_slope.data(0), ray_slope.shape(0),
			height.data(0,0), height.shape(0), height.shape(1)
		);

		return visible;
	});
}