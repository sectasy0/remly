import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

setup(name='remly',
      version='2.0',
      description='Small python library and CLI script which allows running computers remotely on LAN.',
      long_description=(HERE / "README.md").read_text(),
      long_description_content_type="text/markdown",
      author='Piotr Markiewicz',
      keywords=['remly'],
      license='MIT License',
      author_email='sectasy0@gmail.com',
      url='https://github.com/sectasy0/remly',
      packages=find_packages(),
      entry_points={
            'console_scripts': ['remly=remly.main:cli']
        },
      )
