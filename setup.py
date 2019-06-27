from setuptools import setup, find_packages


with open("README.md", 'r') as readme:
	long_description = readme.read()


setup(
	name="rinde",
	description="Library used for creating GUI based on XML and CSS.",
	long_description=long_description,
	version="0.98-B",
	license="MIT License",
	author="Marcin Rajs",
	requires=("pygame", "cssutils"),
	packages=find_packages(
		include="rinde/res",
		exclude=("example_1", "example_2", "example_3")
	)
)
