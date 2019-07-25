import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flashlexiot",
    version="0.9.2",
    author="Clay Graham",
    author_email="claytantor@flashlex.com",
    description="Flashlex IOT for python makes it easy to make any python computer an IOT device.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claytantor/flashlex-iot-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
)
