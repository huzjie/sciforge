# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="sciforge",
    version="1.0.0",
    description="AI 科研智能体与自动化科学发现平台",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={"api": ["fastapi>=0.110.0", "uvicorn[standard]>=0.29.0"]},
    entry_points={"console_scripts": ["sciforge=sciforge.cli:main"]},
)
