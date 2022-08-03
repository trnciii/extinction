#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

#include "kernel.cuh"

PYBIND11_MODULE(gpu, m){
	m.def("visibility", [](const py::array_t<float>& height, const py::array_t<float>& slope){
		const auto& slope_buffer = slope.request();
		py::array_t<float> ret(slope_buffer.shape);
		call_visibility((float*)ret.data(),
			(float*)slope.data(), slope.shape(0),
			(float*)height.data(), height.shape(0), height.shape(1)
		);
		return ret;
	});
}