import setuptools

# setup.py is needed to create a python package
# see https://packaging.python.org/tutorials/packaging-projects/

# read the long description from the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# read the version by executing the _version.py file
# see https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
__version__ = ''
exec(open('src/_version.py').read())

setuptools.setup(
    name="stacasso",
    version=__version__,
    author="Jonathan Driscoll",
    author_email="",
    description="Python library for visualizing Quantum Circuits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jonhub.github.io/stacasso",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)