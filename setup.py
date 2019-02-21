from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_descripton = f.read()

setup(
    name='migrate-exblog',
    version='1.0.0',
    packages=find_packages(),
    long_descripton=long_descripton,
    python_requires='>=3.4',
    include_package_data=True,
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
        'lxml'
    ],
    entry_points='''
        [console_scripts]
        migrate_exblog = migrate_exblog.cli:main
    '''
)
