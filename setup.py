from setuptools import setup, find_packages


setup(
	name="rinde",
	description="Library used for creating GUI based on XML and CSS.",
	version="0.3",
	license="MIT License",
	author="Marcin Rajs",
	
	requires=["pygame", "cssutils"],
	packages=find_packages(exclude=["example_1", "example_2"]),
	package_data={"rinde": ["res/*"]}
)
