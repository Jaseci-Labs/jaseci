from setuptools import setup, find_packages
setup(
    name='jaseci_jskit',
    version='1.3.2.11',
    packages=find_packages(include=['jaseci_jskit', 'jaseci_jskit.*']),
    install_requires=[
        'jaseci',
        'tensorflow >= 2.8.0, < 3.0.0',
        'tensorflow-hub >= 0.12.0, < 1.0.0',
        'tensorflow-text >= 2.7.3, < 3.0.0',
        'transformers >= 4.16.2, < 5.0.0',
        'torch >= 1.10.2, < 2.0.0',
    ],
    package_data={"": ["*.ini"], },
)
