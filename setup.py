'''
THe setup.phy file is an essentil part of oackaging and distributing and
distributing Python projects. It is used by setuptools
(or distutils in older Pyhton versions) to define the configuration of
your project, such as its metadata, dependencies, and more.
setup.py is the build script for your Python project.
It tells setuptools (the standard packaging tool) how to install and distribute your project as a package.

'''

from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    '''
    This function will return list of requements.
    '''
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt','r') as file:
            #Read lines from the file
            lines = file.readlines()
            #Process each line
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and ' -e . ' because this trigering entire setup.py, automatically building entire package 
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement) 
    
    except FileNotFoundError:
        print("Requirements.txt file not found")   
    
    return requirement_lst


# print(get_requirements()) just for test
# now setup our metadata

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author = "Deepak Pandey",
    author_email="deepakpandey28july@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

