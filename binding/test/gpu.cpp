#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

#include "kernel.cuh"

PYBIND11_MODULE(gpu, m){
	m.def("visibility", [](const py::array_t<float>& ar){
		call_visibility((float*)ar.data(), ar.shape(0));
	});
}