import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="algofi-py-sdk",
    description="Algofi Python SDK",
    author="Algofi",
    author_email="owen@algofi.org",
    version="0.0.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Source": "https://github.com/algofi/algofi-py-sdk",
    },
    install_requires=["py-algorand-sdk >= 1.6.0"],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    package_data={'algofi.v1': ['asc.json']},
    include_package_data=True,
)
