from setuptools import setup, find_packages

setup(
    name="rA9",
    version='0.2.8',
    license='GPLv3',
    author="Dongyeong Kim, Jaeseok Lee, Junho Yeo, Yoongi Kim",
    author_email="dongyeongkim33@gmail.com, jepetolee@gmail.com, hanaro0704@gmail.com",
    description="Spiking Neural Network Library based on the spike-based error backpropagation",
    long_description=open('README.md').read(),
    url='https://github.com/MarkusAI/rA9',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],

    install_requires=[
        "jax>=0.2.0",
        "jaxlib>=0.1.55",
        "future>=0.18.2",
        "h5py>=2.3.0",
        "requests>=2.22.0"
    ]

)
