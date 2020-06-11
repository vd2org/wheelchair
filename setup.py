# Copyright (C) 2019-2020 by Vd.
# This file is part of Wheelchair, the async CouchDB connector.
# Wheelchair is released under the MIT License (see LICENSE).


from os.path import join, dirname

import setuptools

setuptools.setup(
    name='wheelchair',
    version='0.1.1',
    author='Vd',
    author_email='vd@vd2.org',
    url='https://github.com/vd2org/wheelchair',
    license='MIT',
    description='The async CouchDB connector written on python.',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    extras_require={
        'aiohttp': ["aiohttp >= 3.6.2"]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
