"""
python setup.py sdist bdist_wheel
"""
import shutil
import sys
from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()
if __name__ == '__main__':
    sys.argv.extend(["sdist", "bdist_wheel", "-d", "./dist/"])
if os.path.exists("./build"):
    shutil.rmtree("./build")
setup(
    name="pipui",
    version="0.2.1",
    description="pipui",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="merlon",
    license="BSD",
    packages=find_packages(),
    package_data={"pipui": ["templates/*", ], },
    install_requires=[
        "flask",
        "requests",
        "beautifulsoup4",

    ],
    setup_requires=["setuptools", "wheel"],
    entry_points={"console_scripts": ["pipui = pipui.server:main"]},
    python_requires=">=3.6, <4",
    cmdclass={},
)
