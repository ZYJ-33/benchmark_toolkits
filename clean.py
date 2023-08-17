import os
import shutil as sh

def remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
        
def remove_dir(dir_path):
    try:
        sh.rmtree(dir_path)
    except FileNotFoundError:
        pass



#remove_file('./BenchmarkGenerator.so')
#remove_file('./libdevice.10.ptx')
remove_file('./module.ptx')
remove_dir('./benchmarks')
remove_dir('./plugin_pass/build')
