# -*- coding: utf-8 -*-
import os
from distutils.core import setup
# genode_version = '2.4b25'
gdal_version = '1.10.1'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
    + '\n')


install_requires = [
    'geonode',
    # 'geonode'.format(genode_version),
    # 'numpy',
    'pygdal=={0}'.format(gdal_version),
]

setup(
    name="imio_geonode",
    version='0.2.26',
    author="",
    author_email="",
    description="imio_geonode, based on GeoNode",
    long_description=long_description,
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Django",
    ],
    license="BSD",
    keywords="imio_geonode geonode django imio",
    url='https://github.com/imio/imio_geonode',
    packages=['imio_geonode',],
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
