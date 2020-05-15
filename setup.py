from setuptools import setup, find_packages

with open("README.md", "r") as fh:

	long_description = fh.read()

setup(

	name='ElectroLens',  

	version='0.1',

	packages=['ElectroLens'],
    #packages=find_packages("ElectroLens"),

    # packages = find_packages(),  
    # # package_dir={'mypkg': 'src/mypkg'},  # didnt use this.
    # package_data = {'static': ['*']},
    include_package_data=True,

	author="Xiangyun (Ray) Lei",

	author_email="xlei38@gatech.edu",

	description="interactive visaulization tool",

	long_description=long_description,

	long_description_content_type="text/markdown",

	url="https://github.com/ray38/NNSubsampling",
    

	classifiers=[
	
		"Programming Language :: Python :: 2",

		"Programming Language :: Python :: 3",

		"License :: OSI Approved :: MIT License",

		"Operating System :: OS Independent",

	],
	
	install_requires=[
		'numpy',
		'scipy',
		'scikit-learn',
        'ase',
        'cefpython3'
	]

 )