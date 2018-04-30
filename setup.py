from setuptools import setup, find_packages

setup(
    name="pyBNS",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        'futures; python_version == "2.7"',
        'future; python_version == "2.7"',
        'urllib3; python_version == "2.7"'
    ],
    author="Vanessa Martinez",
    author_email="datadesk@latimes.com",
    description="A wrapper for the Bloomberg News Service API",
    long_description="Allows python applications to easily connect and interact with the Bloomberg News Service API.",
    url="https://github.com/datadesk/py-bns",
    license="MIT License",
)
