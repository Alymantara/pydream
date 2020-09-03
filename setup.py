import setuptools

# upload to pip
# pip install .
# python3 setup.py sdist bdist_wheel
# twine upload dist/pydream-0.1.8.tar.gz

import os



setuptools.setup(
     name='pydream',
     version='0.1.0',
     packages=['pydream'] ,
     author="Juan V. Hernandez Santisteban",
     author_email="jvhs1@st-andrews.ac.uk",
     description="A python wrapper for Keith Horne's DREAM light curve merging code",
   long_description_content_type="text/markdown",
     url="https://github.com/alymantara/pydream",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         ],
 )
