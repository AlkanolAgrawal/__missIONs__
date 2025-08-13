from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requireds = f.read().splitlines()

setup(
    name='First_Mission',
    version='0.0.1',
    author='Alkanol',
    author_email='coding.alkanol@gmail.com',
    packages=find_packages(),
    install_requires=requireds,
)