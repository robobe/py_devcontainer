from setuptools import find_packages, setup
from app import __version__

setup(
    name="app",
    version=__version__,
    description="description",
    author="",
    author_email="",
    platforms=["any"],
    license="BSD",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "my_app = app.main:main",
        ],
    },
)
