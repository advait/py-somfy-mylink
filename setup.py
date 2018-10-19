import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="somfy_mylink",
    version="0.0.2",
    author="Advait Shinde",
    author_email="advait.shinde@gmail.com",
    description="Python API bindings for the Somfy MyLink Synergy API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/advait/py-somfy-mylink",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries",
    ],
)
