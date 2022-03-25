from setuptools import setup, find_packages
setup(
    name='jaseci',
    version='1.3.1.1',
    packages=find_packages(include=['jaseci', 'jaseci.*']),
    install_requires=[
        'click>=7.1.0,<7.2.0',
        'click-shell>=2.0,<3.0',
        'numpy >= 1.21.0, < 1.22.0',
        'antlr4-python3-runtime>=4.9.0,<4.10.0',
        'requests', 'redis', 'flake8', 'stripe', 'fastapi[all]>=0.73.0,<1.0.0',
        'pydantic'
    ],
    package_data={"": ["*.ini"], },
    entry_points={
        'console_scripts': [
            'jsctl = jaseci.jsctl.jsctl:main'
        ]
    })
