#include <nanobind/nanobind.h>

namespace nb = nanobind;

using namespace nb::literals;

NB_MODULE(core, m) {
    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a);
}
