from setuptools import setup, find_packages

requires = [
    'tornado',
    'tornado-sqlalchemy',
    'psycopg2',
]

setup(
    name='tornado_biothings_explorer_trapi',
    version='0.0',
    description='BioThings_Explorer_TRAPI',
    author='<Your name>',
    author_email='<Your email>',
    keywords='web tornado',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'serve_app = biothings:main',
        ],
    },
)
