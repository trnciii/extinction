# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)


pybind11_add_module(ggx MODULE ggx.cpp)
install(TARGETS ggx DESTINATION .)

add_subdirectory(test)