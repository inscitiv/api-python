from setuptools import setup

setup(
    name='conjurapi',
    version='0.1',
    description='Conjur2 Python API',
    author='Genome Bridge',
    author_email='david@genomebridge.org',
    packages=['conjurapi'],
      long_description="""\
      Conjur2 Python API
      """,
      classifiers=[
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Topic :: Internet",
      ],
      keywords='conjur2',
      license='GPL',
      install_requires=[
        'setuptools',
        'caslib',
        'boto',
        'restkit',
        'pyyaml',
        'requests'
      ],
      )
