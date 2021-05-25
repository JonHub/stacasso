import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stacasso",
    version="0.1.0",
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