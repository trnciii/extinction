#include <nanobind/nanobind.h>
#include <nanobind/tensor.h>
#include <nanobind/stl/vector.h>

#include "kernel.hpp"

namespace nb = nanobind;

using namespace nb::literals;

NB_MODULE(bruteforce, m) {
	m.def("visibility",
		[](nb::tensor<float, nb::shape<nb::any, nb::any>, nb::c_contig, nb::device::cpu> ar,
			nb::tensor<float, nb::shape<nb::any>, nb::c_contig, nb::device::cpu> slope)
		{

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
		}
	);
}
