from setuptools import setup, find_packages

with open("./README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="voyager",
    version="0.0.1-alpha.1",
    description="An async ready wrapper for the NASA Open APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Marwynn Somridhivej",
    author_email="msomridhivej329@gmail.com",
    url="https://github.com/marwynnsomridhivej/voyager",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords='wrapper, api, nasa, http, async, space',
    packages=['voyager'],
    python_requires=">=3.8.0, < 4",
    install_requires=['aiohttp', 'asyncstdlib', 'yarl'],
    extras_require={
        "pil": ['pillow'],
    },
)
