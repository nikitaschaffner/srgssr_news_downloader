from setuptools import setup, find_packages
from srgssr_news_downloader import __version__

with open('LICENSE') as f:
    license = f.read()

setup(
    name            =   'SRG SSR News Downloader',
    version         =   __version__,
    description     =   'Simple Download Tool for the SRG SSR News as audio file.',
    author          =   'Nikita Schaffner',
    author_email    =   'dev@schaffnern.ch',
    url             =   'https://github.com/nikitaschaffner/srgssr_news_downloader',
    license         =   license,
    packages        =   find_packages()
)