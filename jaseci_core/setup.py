from setuptools import setup, find_packages
setup(
    name='jaseci',
    version='0.1.0',
    packages=find_packages(include=['jaseci', 'jaseci.*']),
    install_requires=[
        'click>=7.1.0,<7.2.0', 'click-shell>=2.0,<3.0',
        'numpy >= 1.19.5, < 1.20.0',
        'antlr4-python3-runtime>=4.9.0,<4.10.0',
        'python-logstash>=0.4.6,<0.5',
        'flake8',
    ],
    package_data={"": ["*.ini"], },
    entry_points={
        'console_scripts': [
            'jsctl = jaseci.jsctl.jsctl:main'
        ]
    })
