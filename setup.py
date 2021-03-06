from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='migrate-exblog',
    version='2.0.0',
    packages=find_packages(),
    long_description=long_description,
    python_requires='>=3.4',
    include_package_data=True,
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        migrate-exblog = migrate_exblog.cli:main
    '''
)
