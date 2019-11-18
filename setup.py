from setuptools import setup, find_packages
from codecs import open
from os import path

from unidump import VERSION
from unidump.cli import DESCRIPTION, EPILOG


long_description = DESCRIPTION + '\n\n' + EPILOG

setup(
    name='unidump',
    version=VERSION,

    description='hexdump for your Unicode data',
    long_description=long_description,

    url='https://github.com/Codepoints/unidump',

    author='Manuel Strehl',
    author_email='boldewyn@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Testing',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='unicode hexdump debugging codepoint utility',

    packages=['unidump'],

    package_data={
        'unidump': [
            'locale/de/LC_MESSAGES/unidump.mo',
        ],
    },

    entry_points={
        'console_scripts': [
            'unidump=unidump.cli:main',
        ],
    }
)
