#!/usr/bin/env python3
"""
Setup script for IP Scanner
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ip_scanner",
    version="1.0.0",
    author="Security Research",
    description="Multi-port scanner for IP cameras, DVR, and NVR systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ip-scanner=ip_scanner.main:main",
        ],
    },
)
