from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='SRG SSR News Downloader',
    version='1!1.0.0',
    description='Simple Download Tool for the SRG SSR News as audio file.',
    author='Nikita Schaffner',
    author_email='dev@schaffnern.ch',
    url='https://github.com/nikitaschaffner/srgssr_news_downloader',
    license=license,
    packages=find_packages()
)