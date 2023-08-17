import os
import re
import subprocess
from tabulate import tabulate 


benchmark_dir = './benchmarks'
cubin_pattern = r"\.cubin$"
benchmark_pattern = r"\.cpp$"
cuda_path = '/usr/local/cuda-11.4'
host_compiler = 'g++'
nvcc = cuda_path + '/bin/nvcc'

headers = ["Operator", "RunningTime"]

def compile_benchmark(benchmark_files, excutables):
    for benchmark_file in benchmark_files:
        excutable_benchmark = benchmark_file[0: len(benchmark_file)-4]
        if not excutable_benchmark in excutables:
            print("compiling " + excutable_benchmark)
            subprocess.run(["echo", nvcc, "-ccbin", host_compiler, "-gencode", "arch=compute_86,code=sm_86","-I"+cuda_path+"/include" , "-o", benchmark_dir+'/'+ excutable_benchmark, benchmark_dir+'/'+ benchmark_file, "-L"+cuda_path+"/lib64/stubs", "-lcuda", "-lcudart_static"])
            subprocess.run([nvcc, "-ccbin", host_compiler, "-gencode", "arch=compute_86,code=sm_86","-I"+cuda_path+"/include" , "-o", benchmark_dir+'/'+ excutable_benchmark, benchmark_dir+'/'+ benchmark_file, "-L"+cuda_path+"/lib64/stubs", "-lcuda", "-lcudart_static"])

def run_benchmark(benchmark_files):
    benchmark_runtime = []
    for benchmark_file in benchmark_files:
        excutable_benchmark = benchmark_file[0: len(benchmark_file)-4]
        print("running benchmark: "+excutable_benchmark)
        runtime = subprocess.check_output(["./" + excutable_benchmark], cwd=benchmark_dir)
        benchmark_runtime.append([excutable_benchmark, runtime])
    return benchmark_runtime

def generate_graph_from_data(benchmark_runtimes):
    x_data = list(benchmark_runtimes.keys())
    y_data = [int(value) for value in benchmark_runtimes.values()]
    sns.barplot(x=x_data, y=y_data)
    
    plt.title('operator runtime')
    plt.xlabel('Operator')
    plt.ylabel('Clocks')

    plt.show()

def write_to_file(path, content):
    try:
        with open(path, 'w') as file:
            file.close()
            import os
            os.remove(path)

    except FileNotFoundError:
        pass

    with open(path, 'w') as file:
        file.write(content)


def main():
    benchmark_files = []
    cubin_file = ""
    excutables = set()

    for filename in os.listdir(benchmark_dir):
        if re.search(benchmark_pattern, filename):
            benchmark_files.append(filename)
        elif re.search(cubin_pattern, filename):
            cubin_file = filename
        else: 
            excutables.add(filename)

    compile_benchmark(benchmark_files, excutables);
    benchmark_runtimes = run_benchmark(benchmark_files)
    table = tabulate(benchmark_runtimes, headers=headers, tablefmt="grid")
    write_to_file('./benchmark', table)
    #generate_graph_from_data(benchmark_runtimes)

if __name__ == "__main__":
    main()
