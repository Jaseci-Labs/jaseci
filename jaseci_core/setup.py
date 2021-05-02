from setuptools import setup, find_packages
setup(
    name='jaseci',
    version='0.1.0',
    packages=find_packages(include=['jaseci', 'jaseci.*']),
    install_requires=[
        'click',
    ],
    package_data={"": ["*.ini"], },
    entry_points={
        'console_scripts': [
            'jsctl = jaseci.jsctl.jsctl:main'
        ]
    })
