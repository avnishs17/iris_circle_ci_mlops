from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="iris_mlops",
    version="0.1",
    author="avnishs17",
    packages=find_packages(),
    install_requires = requirements,
)