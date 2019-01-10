from setuptools import setup, find_packages

setup(
    name='absinthe',
    version='0.1dev',
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'absinthe = absinthe:run'
        ]
    },
    install_requires=[
        'pymist',
        'requests',
        'pyquery',
        'furl',
        'termcolor'
    ]
)
