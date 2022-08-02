cmake_minimum_required(VERSION 3.15...3.22)

project(extinction VERSION "0.0.1")


if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path
  # automatically, so we need to add it _or_ the pybind11 specific directory
  # here.
  execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
endif()


set(CMAKE_CXX_STANDARD 20)

find_package(OpenMP REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")


# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(test MODULE binding/test.cpp)

pybind11_add_module(ggx MODULE binding/ggx.cpp)


install(TARGETS test DESTINATION .)
install(TARGETS ggx DESTINATION .)
