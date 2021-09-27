import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__author__ = "PlayerG9"
__version__ = "0.1.0"

setuptools.setup(
    name="mathcompiler",
    version=__version__,
    author=__author__,
    # author_email="author@example.com",
    description="compute user entered equations without leaking access to code like eval() does",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PlayerG9/PyMathCompiler",
    project_urls={
        "Author Github": "https://github.com/PlayerG9",
        "Bug Tracker": "https://github.com/PlayerG9/PyMathCompiler/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"src": "mathcompiler"},
    packages=setuptools.find_packages(where="commandapp"),
    python_requires=">=3.6",
)
