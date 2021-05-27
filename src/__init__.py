# make sure version can be found by typing
#   rhymer.__version__
# read the version by executing the _version.py file
# see https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
# (need to debug this ...)
__version__ = ''
exec(open('src/_version.py').read())
