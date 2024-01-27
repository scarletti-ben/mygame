
# --- This file is not to be run directly, it runs via pip 
    # > pip install . OR python -m pip install .

from setuptools import setup, find_packages

setup(
    name = 'mygame',
    version = '0.1',
    packages = find_packages(),
    description = 'Testing installation of mygame package.',
    url = '#',
    author = 'auth',
    author_email = 'author@email.com',
    license = 'MIT',
    zip_safe = False)