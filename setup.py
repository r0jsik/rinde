from setuptools import setup, find_packages


with open("README.md", "r") as readme:
	long_description = readme.read()


setup(
	name="rinde",
	description="Library used for creating GUI based on XML and CSS.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	version="1.0.1",
	license="MIT License",
	author="Marcin Rajs",
	requires=("pygame", "cssutils"),
	packages=find_packages()
)
