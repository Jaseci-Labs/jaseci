"""Shared input, provenance and CUDA-driver helpers for subtree experiments."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'handwritten_matmul'))
from benchmark import Driver


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2) + '\n')


def read(path):
    return json.loads(Path(path).read_text())


def snapshot():
    return subprocess.check_output(['nvidia-smi'], text=True)


def save_array(directory, name, data):
    a = np.asarray(data, dtype='<i8')
    path = directory / (name + '.bin')
    path.write_bytes(a.tobytes())
    return {'path': path.name, 'dtype': a.dtype.str, 'shape': list(a.shape),
            'bytes': a.nbytes, 'sha256': sha(path)}


def load_array(directory, info):
    path = directory / info['path']
    assert sha(path) == info['sha256'], path
    return np.fromfile(path, dtype=info['dtype']).reshape(info['shape'])


def attributes(driver, fn):
    import ctypes as c
    driver.lib.cuFuncGetAttribute.argtypes = [c.POINTER(c.c_int), c.c_int, c.c_void_p]
    driver.lib.cuFuncGetAttribute.restype = c.c_int
    result = {}
    for name, key in [('local_bytes', 3), ('registers', 4), ('binary_version', 6)]:
        value = c.c_int()
        driver.call('cuFuncGetAttribute', c.byref(value), key, fn)
        result[name] = value.value
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--probe', type=Path, required=True)
    a = p.parse_args()
    d = Driver()
    try:
        result = {'gpu': d.name, 'memory_after_context': d.memory(), 'snapshot': snapshot()}
        write(a.probe, result)
        print(json.dumps(result))
    finally:
        d.close()
