"""`bapsf_qt`"""

__all__ = ["__version__"]

# Enforce Python version check during package import.
# This is the same check as the one at the top of setup.py
import sys

if sys.version_info < (3, 10):  # coverage: ignore
    raise ImportError("bapsf_qt does not support Python < 3.10")

from importlib.metadata import PackageNotFoundError, version

from bapsf_qt import buttons

# define version
try:
    # this places a runtime dependency on setuptools
    #
    # note: if there's any distribution metadata in your source files, then this
    #       will find a version based on those files.  Keep distribution metadata
    #       out of your repository unless you've intentionally installed the package
    #       as editable (e.g. `pip install -e {bapsf_qt_directory_root}`),
    #       but then __version__ will not be updated with each commit, it is
    #       frozen to the version at time of install.
    #
    #: bapsf_qt version string
    __version__ = version("bapsf_qt")
except PackageNotFoundError:
    # package is not installed
    fallback_version = "0.0.0-UNKNOWN"
    try:
        # code most likely being used from source
        # if setuptools_scm is installed then generate a version
        from setuptools_scm import get_version

        __version__ = get_version(
            root="../../", relative_to=__file__, fallback_version="0.0.0"
        )
        del get_version
        warn_add = "setuptools_scm failed to detect the version"
    except ModuleNotFoundError:
        # setuptools_scm is not installed
        __version__ = fallback_version
        warn_add = "setuptools_scm is not installed"

    if __version__ == "0.0.0":
        __version__ = fallback_version
        from warnings import warn

        warn(
            f"bapsf_qt.__version__ not generated (set to 'unknown'), "
            f"bapsf_qt is not an installed package and {warn_add}.",
            RuntimeWarning,
        )

        del warn
    del fallback_version, warn_add
