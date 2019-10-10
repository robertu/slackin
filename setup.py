import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Slack-Integration",
    version="0.0.1",
    author="Mateusz Olkesa",
    description="Kod bota",
    scripts=['scripts/slackin', 'scripts/slackinctl'],
    packages=['slackin'],
    package_dir={'slackin': 'src/slackin'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)