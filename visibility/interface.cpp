#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "kernel.h"

int add(int i, int j) {
	return i + j;
}

namespace py = pybind11;

PYBIND11_MODULE(core, m) {
	m.def("add", add);
	m.def("call_kernel", [](py::array_t<float>& ar){
		call_kernel((float*)ar.data(), ar.size());
	});
}