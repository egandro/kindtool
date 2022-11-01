"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib
from glob import glob

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="kindtool",  # Required
    version="0.0.4",  # Required
    description="Generator for kind k8s clusters",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/egandro/kindtool",  # Optional
    author="Harald Fielker",  # Optional
    author_email="harald.fielker@gmail.com",  # Optional
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="kind, k8s, generator, development",  # Optional
    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    package_dir={"": "src"},  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7, <4",
    install_requires=[
        "argparse",
        "Jinja2",
        "pyyaml"
    ],
    extras_require={  # Optional
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #package_data={  # Optional
    #    "sample": ["package_data.dat"],
    #},
    package_data={
        "kindtool": [ "templates/**", "templates/**/*"]
    },

    # # https://stackoverflow.com/questions/27829754/include-entire-directory-in-python-setup-py-data-files
    # data_files=[("kindtool_templates",
    #     glob('kindtool_templates/**/*', recursive=True), # includes sub-folders - recursive
    # )],  # Optional
    entry_points={  # Optional
        "console_scripts": [
            "kindtool=kindtool.__main__:main"
        ],
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/egandro/kindtool/issues",
        "Source": "https://github.com/egandro/kindtool/",
    },
)
