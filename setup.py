from setuptools import setup, find_packages

setup(
    name='dsctok',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama'
    ],
    python_requires='>=3.6',
)
