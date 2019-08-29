import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codetool",
    version="0.0.1",
    author="lspbupt",
    author_email="lspbupt@sina.com",
    description="A package for project config admin, code generator etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lspbupt/codetool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
