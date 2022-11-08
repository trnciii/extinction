#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

#include <cassert>

#include "kernel.hpp"


PYBIND11_MODULE(cpu, m) {
	m.def("g1_distant", [](const py::array_t<float>& _height, const py::array_t<float>& _ray_slope){
		const auto height = _height.unchecked<2>();
		const auto ray_slope = _ray_slope.unchecked<1>();

		py::array_t<float> visible({ ray_slope.shape(0) });
		auto _vis = visible.mutable_unchecked<1>();

		#pragma omp parallel for schedule(dynamic)
		for(size_t s=0; s<ray_slope.shape(0); s++){
			_vis(s) = kernel::g1_distant((float*)height.data(0, 0), height.shape(0), height.shape(1), ray_slope(s));
		}
		return visible;
	});

	m.def("g1_distant_single", [](
		const py::array_t<float>& _height,
		const py::array_t<size_t>& _starts,
		const py::array_t<float>& _ray_slope)
	{
		const auto height = _height.unchecked<1>();
		const auto starts = _starts.unchecked<1>();
		const auto ray_slope = _ray_slope.unchecked<1>();

		const size_t len = height.shape(0)/2;

		py::array_t<float> visible({ray_slope.shape(0)});
		auto _vis = visible.mutable_unchecked<1>();

		#pragma omp parallel for schedule(dynamic)
		for(size_t s=0; s<ray_slope.shape(0); s++){
			assert(starts(s) < len);
			_vis(s) = kernel::g1_distant_single(
				(float*)height.data(0),
				(size_t*)starts.data(0), starts.shape(0),
				len,
				ray_slope(s)
			);
		}
		return visible;
	});

}
