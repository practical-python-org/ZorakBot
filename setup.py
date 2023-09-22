import setuptools

import versioneer

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
    install_requires=[
        "py-cord",
        "beautifulsoup4",
        "requests",
        "matplotlib",
        "DateTime",
        "pytz",
        "pistonapi",
        "toml",
        "feedparser",
        "html2text",
        "pymongo",
        "PyNaCl==1.5.0",
        "ffmpeg-python==0.2.0",
        "yt-dlp==2023.7.6",
        "googletrans==3.1.0a0",
        "dnspython==2.3.0"
    ],
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
            "distlib==0.3.7",
            "filelock==3.12.4",
            "identify==2.5.29",
            "nodeenv==1.8.0",
            "platformdirs==3.10.0",
            "pre-commit==3.4.0",
            "PyYAML==6.0.1",
            "ruff==0.0.290",
            "virtualenv==20.24.5",
            "versioneer",
        ],
        # 'test': ['coverage'],
    },
)
