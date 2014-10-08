# -*- coding: utf-8 -

import os
from setuptools import setup, find_packages

setup(
    name = 'django-capo',
    version = "0.1",

    description = 'Flexible simple job/task queue engine built on the top of django.',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author = 'Kamil Selwa',
    author_email = 'selwak@gmail.com',
    license = 'MIT',
    url = 'http://selwa.info',

    classifiers = [
        'Development Status :: 1 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: POSIX',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = False,
    packages = find_packages(exclude=['examples', 'tests']),
    #include_package_data = True,
    #package_data={'backfire': media_dirs},
    install_requires=['setuptools', ""],
)