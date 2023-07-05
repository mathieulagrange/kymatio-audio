from setuptools import setup, find_packages
import sys

from importlib.machinery import SourceFileLoader

version = SourceFileLoader('kymatio.version',
                           'kymatio_audio/version.py').load_module()

with open('README.md', 'r') as fdesc:
    long_description = fdesc.read()

setup(
    name='kymatio-audio',
    version=version.version,
    description='Audio processing using kymatio',
    author='Mathieu Lagrange',
    author_email='mathieu.lagrange@ls2n.fr',
    url='https://mathieulagrange.github.io',
    download_url='https://github.com/mathieulagrange/kymatio_audio',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords='experimentation',
    license='ASL',
    install_requires=[
        'numpy',
        'scipy',
        'tqdm',
        'matplotlib',
        'librosa',
        'kymatio',
        'auraloss'
    ],
    python_requires='>=3.6',
    extras_require={
        'docs': ['numpydoc', 'sphinx'],
    }
)