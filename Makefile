CUDA_PATH ?= /usr/local/cuda-11.4/
HOST_COMPILER ?= g++
NVCC ?= $(CUDA_PATH)/bin/nvcc -ccbin $(HOST_COMPILER)
INCLUDE ?= -I$(CUDA_PATH)/include
GENCODE_FLAGS ?= -gencode arch=compute_80,code=sm_80 
LIBRARIES ?= -L$(CUDA_PATH)/lib64/stubs -lcuda -lcudart_static
LLVM_DIR := /home/wanghao44/zhengyujia/compiler/llvm-project-llvmorg-17.0.0-rc1/build/lib/cmake/llvm/ 

MODULE_NAME := $(shell read -p "INPUT MODULE NAME: " module_name && echo $$module_name)
MODULE_LL := $(MODULE_NAME).ll
PTX_COMPILER := llc
GPU_ARCH := sm_86
PTX_TYPE := nvptx64
PTX_ASSMBLER := ptxas
NVCC := nvcc

$(MODULE_NAME).ptx: $(MODULE_LL)
	$(PTX_COMPILER) -mcpu=$(GPU_ARCH)  -march=$(PTX_TYPE) $< -o $@

libdevice.10.ptx: libdevice.10.ll
	$(PTX_COMPILER) -mcpu=$(GPU_ARCH)  -march=$(PTX_TYPE) $< -o $@

$(MODULE_NAME).cubin: $(MODULE_NAME).ptx libdevice.10.ptx
	$(NVCC) -arch=$(GPU_ARCH) -dlink -cubin $^ -o $@

BenchmarkGenerator.so: 
	cmake ./plugin_pass -B./plugin_pass/build -DLLVM_DIR=$(LLVM_DIR)
	@$(MAKE) -C./plugin_pass/build
	cp ./plugin_pass/build/$@ ./

generate_benchmark: $(MODULE_NAME).cubin BenchmarkGenerator.so
	opt --load-pass-plugin=BenchmarkGenerator.so --passes="BenchMark-Generator" -disable-output $(MODULE_LL)
	mv ./$< ./benchmarks/$<

run: generate_benchmark
	python3 ./run.py
	
clean:
	python3 ./clean.py
