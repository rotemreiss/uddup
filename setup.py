from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="uddup",
    version="0.9.3",
    author="Rotem Reiss",
    author_email="reiss.r@gmail.com",
    description="URLs Deduplication Tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rotemreiss/uddup",
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'uddup=uddup.main:interactive',
        ],
    },
)
