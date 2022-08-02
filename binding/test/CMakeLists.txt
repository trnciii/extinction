# cpu
pybind11_add_module(cpu MODULE cpu.cpp)
install(TARGETS cpu DESTINATION ./test)


find_package(CUDA)
if(CUDA_FOUND)
	cuda_add_library(kernel kernel.cu)

	pybind11_add_module(gpu MODULE gpu.cpp)
	target_link_libraries(gpu PRIVATE kernel )
	install(TARGETS gpu DESTINATION ./test)
endif()