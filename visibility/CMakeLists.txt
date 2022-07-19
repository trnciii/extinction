cmake_minimum_required(VERSION 3.4...3.18)
project(visibility)


set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")


set(PYBIND11_PYTHON_VERSION 3.9)
add_subdirectory(pybind11)
pybind11_add_module(core interface.cpp)


find_package(CUDA)
cuda_add_library(kernel kernel.cu)

target_link_libraries(core PRIVATE kernel)