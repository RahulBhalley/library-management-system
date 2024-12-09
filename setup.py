from setuptools import setup, find_packages

setup(
    name='library-management-system',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pyjwt',
        'pytest',
        'requests',
        'typing',
        'hashlib',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'library-cli=library_cli:main',
        ],
    }
)