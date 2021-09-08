import os
import sys
from pathlib import Path

import cmake_build_extension
import setuptools

try:
    # force this package to be interpreter and abi independent
    # https://newbedev.com/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def get_tag(self):
            impl, abi, plat = _bdist_wheel.get_tag(self)
            return ('py3', 'none', plat)
except ImportError:
    bdist_wheel = None

init_py = """
import pathlib

INSTALL_DIR = pathlib.Path(__file__).parent
LIB_DIR = INSTALL_DIR / "lib"
INCLUDE_DIR = INSTALL_DIR / "include"
"""

# This example is compliant with PEP517 and PEP518. It uses the setup.cfg file to store
# most of the package metadata. However, build extensions are not supported and must be
# configured in the setup.py.
setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="ogdf-build-debug",
            # Name of the resulting package name (import ogdf_build_debug)
            install_prefix="ogdf_build_debug",
            # Writes the content to the top-level __init__.py
            write_top_level_init=init_py,
            # Selects the folder where the main CMakeLists.txt is stored
            # (it could be a subfolder)
            source_dir=str(Path(__file__).parent.absolute()),
            cmake_configure_options=[
                "-DCMAKE_INSTALL_LIBDIR=lib",
                "-DBUILD_SHARED_LIBS=ON",
                "-DDOC_INSTALL=OFF",
                "-DCMAKE_BUILD_TYPE=Debug",
                "-DOGDF_USE_ASSERT_EXCEPTIONS=ON",
                # "-DOGDF_USE_ASSERT_EXCEPTIONS_WITH_STACK_TRACE=ON_LIBUNWIND",
            ],
        ),
    ],
    cmdclass=dict(
        # Enable the CMakeExtension entries defined above
        build_ext=cmake_build_extension.BuildExtension,
        bdist_wheel=bdist_wheel
    ),
)
