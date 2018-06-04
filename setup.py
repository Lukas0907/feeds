from setuptools import find_packages, setup

setup(
    name="feeds",
    version="2017.08.14",
    # Author details
    author="Florian Preinstorfer, Lukas Anzinger",
    author_email="florian@nblock.org, lukas@lukasanzinger.at",
    url="https://github.com/nblock/feeds",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click>=6.6",
        "Delorean>=0.6.0",
        "Scrapy>=1.1",
        "scrapy-inline-requests>=0.3.1",
        "bleach>=1.4.3",
        "dateparser>=0.5.1",
        "lxml>=3.5.0",
    ],
    extras_require={
        "doc": ["doc8", "restructuredtext_lint", "sphinx", "sphinx_rtd_theme"],
        "test": ["flake8", "black", "isort"],
    },
    entry_points="""
        [console_scripts]
        feeds=feeds.cli:main
    """,
)
