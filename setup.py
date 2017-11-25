import os.path
from setuptools import setup, find_packages

__DIR__ = os.path.abspath(os.path.dirname(__file__))

setup(
    name = 'pgstorm',
    version = '0.0.1a1',
    description = 'A PostgreSQL load tester',
    url = 'https://github.com/mikeshultz/pgstorm',
    author = 'Mike Shultz',
    author_email = 'mike@mikeshultz.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords = 'postgresql database load test sql',
    packages = find_packages(exclude = ['build', 'dist']),
    install_requires = ['psycopg2>=2.7.3.2'],
    entry_points = {
        'console_scripts': ['pgstorm=pgstorm:main'],
    }
)