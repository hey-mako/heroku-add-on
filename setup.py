from setuptools import find_packages, setup


setup(
    install_requires=[
        'Flask==1.0.2',
        'pymongo==3.7.1',
    ],
    name='add-on',
    packages=find_packages(),
    tests_require=[
        'pylint==2.1.1',
    ]
)
