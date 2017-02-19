from setuptools import setup

setup(
    name='cliboy_queue',
    version='0.1',
    py_modules=['cliboy_queue'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
    cliboy_queue=cliboy_queue:cli
    ''',
)
