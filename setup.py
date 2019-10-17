from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Slack Integration Bot",
    version="0.1.1",
    author="Mateusz Oleksa",
    author_email="mail@linacti.software",
    keywords="slack flask bot",
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