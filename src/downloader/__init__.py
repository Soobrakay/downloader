"""
downloader
==========

Creates the command line interface for downloading workouts or podcasts.
"""
import click

from .pn import precision_nutrition
from .talkpython import podcast


@click.group()
def cli():
    pass


cli.add_command(precision_nutrition)
cli.add_command(podcast)
