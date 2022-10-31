from setuptools import setup, find_packages

setup(
    name='alan-cli',
    version='0.1.4',
    include_package_data=True,
    python_requires='>=3.10.0',
    license='MIT',
    author="Alan Dao",
    author_email='contact@daogiatuan.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/tikikun/cli_tools',
    keywords='cli tool',
    entry_points={
        'console_scripts': [
            'alan-cli = program.main:main',
        ]
    },
    install_requires=[
        'beautifulsoup4==4.11.1', 'feedparser==6.0.10', 'rich==12.6.0', 'typer==0.6.1'
    ],

)
