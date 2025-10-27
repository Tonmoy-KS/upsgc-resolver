# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="upsgc-resolver",
    version="1.0.0",
    author="Tonmoy-KS",
    author_email="tonmoyks.3755@gmail.com", 
    description="A VS debating system and auto-resolver based on the UPSGC framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tonmoy_KS/upsgc-resolver", 
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.0.0",
        "numpy>=1.18.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'start-upsgc_resolve = upsgc_resolver.resolver:main',
        ],
    },
)