import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-questionnaire",
    version="0.0.1",
    description="A Django application for creating simple online questionnaires/surveys.",
    long_description=read("README.md"),
    author="Marco Minutoli",
    author_email="info@marcominutoli.it",
    license="BSD",
    url="https://github.com/Bookrepublic/django-questionnaire",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Framework :: Django",
    ],
    install_requires=[
        'django',
    ],
)
