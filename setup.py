from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('jishaku_nextcord/meta.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='jishaku_nextcord',
      author='This is not Reidy',
      url='https://github.com/This-is-not-Reidy/jishaku-nextcord.git',
      project_urls={
        "Author Discord": "https://discord.com/users/848593011038224405",
      },
      version=version,
      packages=['jishaku_nextcord'],
      description='This is a fork of jishaku for nextcord',
      long_description=readme,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      )
