import os
import pathlib
import re
import subprocess

from setuptools import setup

ROOT = pathlib.Path(__file__).parent

with open(ROOT / 'jishaku' / 'meta.py', 'r', encoding='utf-8') as f:
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
