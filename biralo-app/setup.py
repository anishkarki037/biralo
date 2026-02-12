"""
Setup script for Biralo Desktop App
"""
from setuptools import setup, find_packages

setup(
    name="biralo-desktop",
    version="1.0.0",
    description="Desktop application for Biralo AI Assistant",
    author="Biralo Contributors",
    python_requires=">=3.11",
    install_requires=[
        "customtkinter>=5.2.0",
        "biralo-ai>=0.1.3",
    ],
    entry_points={
        "console_scripts": [
            "biralo-desktop=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
