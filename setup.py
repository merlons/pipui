"""
python setup.py sdist bdist_wheel
"""
import os
import shutil
import sys
from setuptools import setup, find_packages
from datetime import datetime
from setuptools.command.install import install
import subprocess
import os

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()
if __name__ == '__main__':
    sys.argv.extend(["sdist", "bdist_wheel", "-d", "./dist/"])
if os.path.exists("./build"):
    shutil.rmtree("./build")
setup(
    name="pipui",
    # version=datetime.now().strftime("%Y%m%d"),
    version="0.1.7",
    description="pipui",
    long_description=long_description,
    author="merlon",
    license="BSD",
    packages=find_packages(),
    # packages=["pygcbs"],
    package_data={"pipui": ["templates/*", ], },
    # include_package
    install_requires=[
        "uvicorn",
        "jinja2",
        "fastapi",
        "requests",
        "beautifulsoup4",

    ],
    setup_requires=["setuptools", "wheel"],
    entry_points={"console_scripts": ["pipui = pipui.main:main"]},
    python_requires=">=3.6, <4",
    # include_package_data=True,
    cmdclass={
        # "install": PostInstallCommand,
    },
)
