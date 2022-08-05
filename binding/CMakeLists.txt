set(CMAKE_CXX_STANDARD 20)

find_package(OpenMP REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)


pybind11_add_module(ggx MODULE ggx.cpp)
install(TARGETS ggx DESTINATION .)

add_subdirectory(test)