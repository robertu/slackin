import setuptools

with open("docs/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Slack-Integration",
    version="0.0.1",
    author="Mateusz Olkesa",
    description="Kod bota",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)