
--- Package Structure
    parent_directory/
    │
    ├── package_name/
    │  │
    │  ├── __init__.py
    │  ├── locals.py
    │  ├── constants.py
    │  ├── functions.py
    │  ├── classes.py
    │
    ├── __init__.py
    ├── setup.py
    ├── readme.txt
  > ├── install.py > My custom script to install the package without the use of command line

--- How to Install Python Packages via Command Line
    < Change directory to the directory where setup.py resides
        < cd parent_folder
    < Install the package to Python PATH
        < pip install .
    < Or install the package with a given python version
        < python -m pip install . > python -m tells the interpreter to run the script as a module, and specifies a python version

--- How to Install Python Packages via Custom Script
    < Run setup.py in the parent_directory
    < Answer prompts on whether or not you want the package to be editable / in development mode

--- Installing Python Packages in Editable / Development Mode
    < To install in editable mode add the editable tag "-e" 
        < pip install -e .
        < This creates a link to the original files allowing you to change them and see the results
    < This will create a file in \AppData\Local\Programs\Python\Python310\Lib\site-packages:
        > package_name.egg-link
    < This egg-link file will tell your computer where to find the package files
    < This allows you to edit them while still allowing scripts to access them
    * Once done it is important to install the package without the editable tag

--- Foldered Package Structure
    parent_directory/
    │
    ├── package_name/
    │   │
    │   ├── folder_one/
    │   │  │
   <│   │  ├── __init__.py < init in folder_one
    │   │  ├── locals.py
    │   │  ├── constants.py
    │   │
    │   ├── folder_two/
    │   │  │
   <│   │  ├── __init__.py < init in folder_two
    │   │  ├── functions.py
    │   │  ├── classes.py
    │   │
   <│   ├── __init__.py < init in package_directory
    │
    ├── setup.py
    ├── readme.txt
    ├── install.py

< Default Layout for setup.py

from setuptools import setup

setup(name = 'package_name',
version = '0.1',
description = 'Testing installation of package called package_name.',
url = '#',
author = 'auth',
author_email = 'author@email.com',
license = 'MIT',
packages = ['package_name'],
zip_safe = False)

< Usage of install.py
    < Runs via VSCode F5 to Run Python File
    < Prompts the user if they want to install in editable mode or normal mode

--- Fixing __init__.py in Foldered Packages
    foldered_package_template/
    │
    ├── foldered/
    │   │
    │   ├── core/
    │   │  │
   <│   │  ├── __init__.py #B1
    │   │  ├── initialisation.py
    │   │
    │   ├── draw/
    │   │  │
   <│   │  ├── __init__.py #B2
    │   │  ├── rectangle.py
    │   │
    │   ├── experimental/
    │   │  │
   <│   │  ├── __init__.py < #B3
    │   │  ├── experimental.py
    │   │
    │   ├── maths/
    │   │  │
   <│   │  ├── __init__.py < #B4
    │   │  ├── angles.py
    │   │  ├── lines.py
    │   │  ├── points.py
    │   │
    │   ├── sprite/
    │   │  │
   <│   │  ├── __init__.py < #B5
    │   │  ├── enemy.py
    │   │  ├── entity.py
    │   │  ├── player.py
    │   │  ├── sprite.py
    │   │
   >│   ├── __init__.py < #A1
    │
    ├── setup.py
    ├── readme.txt
    ├── install.py

> __init__ A1 should read
from . import draw, core, experimental, maths, sprite

< __init__ B1 should read
from . import initialisation

< __init__ B2 should read
from . import rectangle

< __init__ B3 should read
from . import experimental

< __init__ B4 should read
from . import angles, lines, points

< __init__ B5 should read
from . import sprite, entity, player, enemy

< You need to directly import folders to each outermost __init__.py
    < This is done with:
        > from . import folder_name

< You need to directly import modules to each innermose __init__.py
    < This is done with:
        > from . import module_name
    