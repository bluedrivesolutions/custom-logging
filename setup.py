# setup.py
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="custom-logging",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Hilario Petalbo, II",
    author_email="hilario@bluedrive.ph",
    description="A simple Django model logger",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
