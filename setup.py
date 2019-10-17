from setuptools import setup, find_packages


long_description = '''
Slack integration bot based on flask appliacation.
Requires external ip to operate and quite comprehensive configuration on slack side.
It can operate on public channels as well as in private conversations.

Supports:

* commands
* slack forms
* text replies
* atachements
'''

setup(
    name="Slack Integration Bot",
    version="0.1.2",
    author="Mateusz Oleksa & Robert Urbanczyk",
    author_email="mail@linacti.software",
    keywords="slack flask bot",
    license = 'LGPL',
    platforms = ['Linux','Mac OSX'],
    description="An implementation of simple slack integration bot",
    packages=find_packages('src'),
    package_dir={'':'src'},
    long_description=long_description,
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'cairosvg',
        'pycairo',
        'slackeventsapi',
        'slackclient',
        'pillow',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'slackin-bot = slackin.bot:main',
        ],
    },
)