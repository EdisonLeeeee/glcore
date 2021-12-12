from torch.utils.cpp_extension import BuildExtension, CppExtension, CUDAExtension
from torch.__config__ import parallel_info
from setuptools import setup, find_packages

import sys
import os

VERSION = "0.1.0"
url = 'https://github.com/EdisonLeeeee/glcore'


install_requires = [
    'torch',
    'scipy',
    'numpy',
    'pandas',
]

setup_requires = ['pytest-runner']
tests_require = ['pytest', 'pytest-cov']

extra_compile_args = {'cxx': ['-O2']}
extra_link_args = ['-s']

nvcc_flags = os.getenv('NVCC_FLAGS', '')
nvcc_flags = [] if nvcc_flags == '' else nvcc_flags.split(' ')
nvcc_flags += ['--expt-relaxed-constexpr', '-O2']
extra_compile_args['nvcc'] = nvcc_flags

if sys.platform == 'win32':
    extra_link_args += ['cusparse.lib']
else:
    extra_link_args += ['-lcusparse', '-l', 'cusparse']


info = parallel_info()
if ('backend: OpenMP' in info and 'OpenMP not found' not in info
        and sys.platform != 'darwin'):
    extra_compile_args['cxx'] += ['-DAT_PARALLEL_OPENMP']

    if sys.platform == 'win32':
        extra_compile_args['cxx'] += ['/openmp']
    else:
        extra_compile_args['cxx'] += ['-fopenmp']
else:
    print('Compiling without OpenMP...')

setup(
    name='glcore',
    version=VERSION,
    description='A graph learning toolxbox.',
    author='Jintang Li',
    author_email='lijt55@mail2.sysu.edu.cn',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, VERSION),
    keywords=[
        'pytorch',
        'toolbox',
        'geometric-deep-learning',
        'graph-neural-networks',
    ],
    python_requires='>=3.6',
    license="MIT LICENSE",
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    packages=find_packages(exclude=("examples", "imgs", "benchmark", "test")),
    ext_modules=[
        CppExtension("glcore.sampler", sources=["csrc/cpu/neighbor_sampler_cpu.cpp"], extra_compile_args=['-g']),
        CUDAExtension("glcore.ops",
                      sources=["csrc/cuda/ops.cpp", "csrc/cuda/ops_kernel.cu"],
                      extra_compile_args=extra_compile_args,
                      extra_link_args=extra_link_args)
    ],
    cmdclass={
        'build_ext':
        BuildExtension.with_options(no_python_abi_suffix=True, use_ninja=False)
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
