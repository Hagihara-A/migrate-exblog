from setuptools import setup, find_packages
setup(name='scrape-excite-blog',
      version='1.0.0',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'requests',
          'beautifulsoup4',
          'tqdm'
      ])
