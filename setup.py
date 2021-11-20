from torch.utils.cpp_extension import BuildExtension
from torch.utils.cpp_extension import CppExtension
from setuptools import setup, find_packages

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

    ],
    cmdclass={
        'build_ext':
        BuildExtension
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
