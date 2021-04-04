"""
common
======

Functions used across both downloaders.
"""
import os
import typing

import click
import requests


def download(href: str) -> bytes:
    """Get the content of a link.

    :param href: URL to download.
    :returns: contents of the file as bytes on success.
        Empty bytes on failure.
    """
    response = requests.get(href)
    return response.content if response.ok else b""


def download_if_missing(local_remote: typing.Tuple[str, str]) -> typing.NoReturn:
    """Download a remote file if no local copy exists.

    :param local_remote: tuple of (local, remote).
        ``local`` is the name of the file to check or write locally.
        ``remote`` is the URL of the file to download if no local copy exists.
    """
    local, remote = local_remote
    if os.path.exists(local):
        click.echo(f"{local} already exists.")
        return
    click.echo(f"Downloading {remote} to {local}")
    write_content_to_file(download(remote), local)
    click.echo(f"Downloaded {remote} to {local}")


def write_content_to_file(content: bytes, name: str) -> typing.NoReturn:
    """Writes `content` to `name` file.

    :param content: File contents to write out.
    :param name: Name of the file to write.
    """
    with open(name, mode="wb") as f:
        f.write(content)
