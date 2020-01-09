import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flashlexiot",
    version="0.9.3",
    author="Clay Graham",
    author_email="claytantor@flashlex.com",
    description="Flashlex IOT for python makes it easy to make any python computer an IOT device.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claytantor/flashlex-iot-python",
    packages=setuptools.find_packages(),
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],

)
