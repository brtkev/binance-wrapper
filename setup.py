from setuptools import setup
import json

with open("version.json", "r") as f:
    version = json.loads(f.read())

setup(**version)