import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flashlexpi",
    version="0.9.1",
    author="Clay Graham",
    author_email="claytantor@flashlex.com",
    description="Flashlex pi for python makes it easy to make your Rasberry Pi an IOT device.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claytantor/flashlex-pi-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
)