from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proveit",
    version="0.1.0",
    author="ProveIt Team",
    author_email="info@proveit.example.com",
    description="A blockchain-based intellectual property verification system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/proveit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.7",
    install_requires=[
        "web3>=6.0.0",
        "click>=8.0.0",
        "pycryptodome>=3.15.0",
        "reportlab>=3.6.0",
        "flask>=2.0.0",
        "requests>=2.27.0",
    ],
    entry_points={
        "console_scripts": [
            "proveit=proveit.cli:main",
        ],
    },
    include_package_data=True,
)
