from setuptools import setup
from setuptools import find_packages


setup(
	name="rinde",
	description="Library used for creating GUI based on XML and CSS.",
	version="0.42",
	license="MIT License",
	author="Marcin Rajs",
	
	requires=["pygame", "cssutils"],
	packages=find_packages(
		include="rinde/res",
		exclude=["example_1", "example_2"]
	)
)
