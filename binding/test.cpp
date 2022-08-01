#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(test, m) {
	m.def("visibility", [](const py::array_t<float>& _ar, const py::array_t<float>& _slope){
		const auto ar = _ar.unchecked<2>();
		const auto slope = _slope.unchecked<1>();

		std::vector<float> visible(slope.shape(0));

		#pragma omp parallel for schedule(dynamic)
		for(size_t s=0; s<slope.shape(0); s++){
			visible[s] = ar.shape(0);

			for(size_t m=0; m<ar.shape(0); m++){
				for(size_t i=0; i<ar.shape(1); i++){
					if( ar(m, 0) + slope(s)*i < ar(m, i) ){
						visible[s] -= 1;
						break;
					}
				}
			}

			visible[s] /= ar.shape(0);
		}
		return visible;
	});

}
