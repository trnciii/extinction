#include <nanobind/nanobind.h>
#include <nanobind/tensor.h>

#include "kernel.hpp"

namespace nb = nanobind;

using namespace nb::literals;

NB_MODULE(bruteforce, m) {
	m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a);
	m.def("call_kernel", [](nb::tensor<float, nb::shape<nb::any>, nb::c_contig, nb::device::cpu> ar){
		kernel((float*)ar.data(), ar.shape(0));
	});
}
