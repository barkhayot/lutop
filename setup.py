from setuptools import setup, find_packages

setup(
    name="lutop",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "lutop = lutop.lutop:main",
        ],
    },
    python_requires=">=3.6",
    description="A utility to monitor system resources and top processes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Barkhayot Juraev",
    author_email="barkhayotoff@email.com",
    url="https://github.com/barkhayot/lutop",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="system monitor processes",
)
