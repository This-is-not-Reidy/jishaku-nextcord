#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License
Copyright (c) 2021 Devon (Gorialis) R
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import pathlib
import re
import subprocess

from setuptools import setup

ROOT = pathlib.Path(__file__).parent

with open(ROOT / 'jishaku_nextcord' / 'meta.py', 'r', encoding='utf-8') as f:
    VERSION_MATCH = re.search(r'VersionInfo\(major=(\d+), minor=(\d+), micro=(\d+), .+\)', f.read(), re.MULTILINE)

    if not VERSION_MATCH:
        raise RuntimeError('version is not set or could not be located')

    VERSION = '.'.join([VERSION_MATCH.group(1), VERSION_MATCH.group(2), VERSION_MATCH.group(3)])

EXTRA_REQUIRES = {}

for feature in (ROOT / 'requirements').glob('*.txt'):
    with open(feature, 'r', encoding='utf-8') as f:
        EXTRA_REQUIRES[feature.with_suffix('').name] = f.read().splitlines()

REQUIREMENTS = EXTRA_REQUIRES.pop('_')

if not VERSION:
    raise RuntimeError('version is not set')


try:
    PROCESS = subprocess.Popen(
        ['git', 'rev-list', '--count', 'HEAD'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    COMMIT_COUNT, ERR = PROCESS.communicate()

    if COMMIT_COUNT:
        PROCESS = subprocess.Popen(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        COMMIT_HASH, ERR = PROCESS.communicate()

        if COMMIT_HASH:
            match = re.match(r'(\d).(\d).(\d)(a|b|rc)?', os.getenv('tag_name') or "")

            if (match and match[4]) or not match:
                VERSION += ('' if match else 'a') + COMMIT_COUNT.decode('utf-8').strip() + '+g' + COMMIT_HASH.decode('utf-8').strip()

                # Also attempt to retrieve a branch, when applicable
                PROCESS = subprocess.Popen(
                    ['git', 'symbolic-ref', '-q', '--short', 'HEAD'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                COMMIT_BRANCH, ERR = PROCESS.communicate()

                if COMMIT_BRANCH:
                    VERSION += "." + re.sub('[^a-zA-Z0-9.]', '.', COMMIT_BRANCH.decode('utf-8').strip())

except FileNotFoundError:
    pass


with open(ROOT / 'README.md', 'r', encoding='utf-8') as f:
    README = f.read()


setup(
    name='jishaku_nextcord',
    author='This is not Reidy',
    url='https://github.com/This-is-not-Reidy/jishaku-nextcord.git',
    description='This is a fork of jishaku for nextcord',
    long_description=README,
    long_description_content_type='text/markdown',
    version=VERSION,
    packages=['jishaku_nextcord', 'jishaku_nextcord.features', 'jishaku_nextcord.repl', 'jishaku_nextcord.shim'],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires='>=3.8.0',

    extras_require=EXTRA_REQUIRES
)
