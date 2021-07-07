from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setup(
    name='ldcoolp-figshare',
    version='0.3.2',
    packages=find_namespace_packages(),
    url='https://github.com/UAL-RE/ldcoolp-figshare/',
    project_urls={
        'Source': 'https://github.com/UAL-RE/ldcoolp-figshare/',
        'Documentation': 'https://ldcoolp-figshare.readthedocs.io/',
        'Tracker': 'https://github.com/UAL-RE/ldcoolp-figshare/issues',
    },
    license='MIT License',
    author='Chun Ly',
    author_email='astro.chun@gmail.com',
    description='Python tool using the Figshare API for data curation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
