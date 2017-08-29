from setuptools import setup, find_packages


setup(
	name="rinde",
	description="Library which can be used for creating GUI based on XML and CSS.",
	version="0.2",
	license="MIT License",
	author="Marcin Rajs",
	
	requires=["pygame", "cssutils"],
	packages=find_packages(exclude=["example_1"]),
	package_data={"rinde": ["res/*"]}
)
