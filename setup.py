from setuptools import setup, find_packages


setup(
    name='hotcake',
    version='0.0.1',
    description='HTTP and SSH proxy server',
    author='NAKAMURA Yoshitaka',
    author_email='arumakanoy@gmail.com',
    licence='BSD-2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'hotcake = hotcake.main:main',
        ],
    },
    install_requires=[
        'Twisted',
        'click',
        'cryptography',
    ],
)
