#!/usr/bin/env python

import os
from typing import List

from setuptools import find_packages, setup

VERSION = "0.1.1"


def generate_install_requires() -> List[str]:
    # Path agnostic way to open requirements
    abspath = os.path.abspath(__file__)
    project_root = os.path.dirname(abspath)
    req_path = os.path.join(project_root, "requirements.txt")

    with open(req_path) as f:
        required = f.read().splitlines()

    # Remove github deps and comments
    return list(filter(lambda x: not x.startswith("#"), required))


setup(
    name="github-token-app",
    version=VERSION,
    description="A github app wrapper to generate short lived token",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mercari",
    url="https://github.com/mercari/github-token-app",
    packages=find_packages(),
    package_data={"github_token_app": ["py.typed"]},
    install_requires=generate_install_requires(),
    zip_safe=False,
    include_package_data=True,
    entry_points={"console_scripts": ["gta = github_token_app.cli:main"],},
)
