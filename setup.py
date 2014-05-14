import os
import re
from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)

setup(
    name="django-crudwrapper",
    version=get_version('crudwrapper'),
    description="Wrappers for Django CRUD work.",
    long_description="A collection of wrapper to 3rd party Django apps for CRUD work.",
    keywords="django, views, forms, mixins",
    author="Jerick Don San Juan <jerick@icannhas.com>",
    author_email="jerick@icannhas.com",
    url="https://github.com/jericksanjuan/django-crudwrapper",
    license="",
    packages=["crudwrapper"],
    zip_safe=False,
    install_requires=[
        "Django >= 1.4.1",
        "django-braces >= 1.4.0",
        "django-extra-views >= 0.6.4",
        "django-vanilla-views >= 1.0.2",
        "django-crispy-forms >= 1.4.0",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
