import pathlib

import pkg_resources
import setuptools

import versioneer

install_requires = []
with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]


setuptools.setup(
    name="zorak",
    description="An installable version of the Zorak.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    entry_points={"console_scripts": ["zorak=zorak.__main__:main"]},
    package_data={"": ["*.toml"]},
    install_requires=install_requires,
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "cfgv==3.4.0",
            "distlib==0.3.8",
            "filelock==3.15.1",
            "identify==2.6.0",
            "nodeenv==1.9.1",
            "platformdirs==4.2.2",
            "pre-commit==3.7.1",
            "PyYAML==6.0.1",
            "ruff==0.4.9",
            "virtualenv==20.26.2",
            "versioneer",
        ],
        # 'test': ['coverage'],
    },
)
