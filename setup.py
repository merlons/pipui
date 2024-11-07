"""
python setup.py sdist bdist_wheel
"""
import shutil
import sys
import os
from setuptools import setup, find_packages


# 获取项目的长描述内容
def get_long_description():
    try:
        with open("README.md", "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Long description not available."


# 清理构建目录
def clean_build():
    build_dirs = ['./build', './dist', './pipui.egg-info']
    for directory in build_dirs:
        if os.path.exists(directory):
            shutil.rmtree(directory)


# 从 requirements.txt 读取依赖
def read_requirements():
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []


# 主程序入口
def main():
    clean_build()
    setup(
        name="pipui",
        version="0.2.2",  # 版本号
        description="A simple Python package management tool",
        long_description=get_long_description(),
        long_description_content_type='text/markdown',
        author="merlon",
        license="BSD",
        packages=find_packages(),
        package_data={"pipui": ["templates/*", ]},
        install_requires=read_requirements(),  # 从 requirements.txt 读取依赖
        setup_requires=["setuptools", "wheel"],
        entry_points={"console_scripts": ["pipui = pipui.server:main"]},
        python_requires=">=3.6, <4",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
        ],
        url="https://github.com/merlons/pipui.git",  # 项目主页或 GitHub 仓库地址
    )


if __name__ == "__main__":
    sys.argv.extend(["sdist", "bdist_wheel", "-d", "./dist/"])
    main()
