from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_descripton = f.read()

setup(name='migrate-excite-blog',
      version='1.0.0',
      packages=find_packages(),
      long_descripton=long_descripton,
      long_descripton_content_type='',
      python_requires='>=3.4',
      include_package_data=True,
      install_requires=[
          'requests',
          'beautifulsoup4',
          'tqdm'
      ])
