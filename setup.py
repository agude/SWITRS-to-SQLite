#!/usr/bin/env python3

import re
from setuptools import setup


# Get the version from the main script
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open("switrs_to_sqlite/switrs_to_sqlite.py").read(),
    re.M,
).group(1)


# Try to import pypandoc to convert the readme, otherwise ignore it
try:
    import pypandoc

    long_description = pypandoc.convert("README.md", "rst")
except ImportError:
    long_description = ""


# Configure the package
setup(
    name="switrs-to-sqlite",
    version=version,
    description="Script for converting SWITRS reports to SQLite.",
    long_description=long_description,
    author="Alexander Gude",
    author_email="alex.public.account@gmail.com",
    url="https://github.com/agude/SWITRS-to-SQLite",
    license="GPLv3+",
    platforms=["any"],
    packages=["switrs_to_sqlite"],
    entry_points={
        "console_scripts": [
            "switrs_to_sqlite = switrs_to_sqlite.switrs_to_sqlite:main"
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
    keywords=[
        "switrs",
        "sqlite",
        "data",
    ],
    setup_requires=[
        "pypandoc",
        "pytest-runner",
    ],
    tests_require=["pytest"],
    python_requires=">=3.6, <4",
)
