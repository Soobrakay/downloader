#!/usr/bin/env python3
"""
talkpython
==========

This script will crawl and download all podcast MP3s for TalkPython.fm.
"""
import functools
import multiprocessing
import os
import re
import sys

import click
import requests
from bs4 import BeautifulSoup as bs
from more_itertools import first_true

#: Regex to find the name of the .mp3 file to download.
MP3_MATCHER = re.compile(r"/([^/]*.mp3)", re.IGNORECASE)


def is_show_href(href):
    """Returns True for links with hrefs to show pages"""
    return href and "/episodes/show/" in href.lower()


def ends_in_mp3(href):
    return href and href.endswith(".mp3")


def write_mp3(content, name):
    """Writes MP3 `content` to `name` file"""
    with open(name, mode="wb") as mp3_file:
        mp3_file.write(content)


def download(href):
    """Get the content of an mp3 link"""
    response = requests.get(href)
    return response.content if response.ok else ""


def mp3_name(href, test=MP3_MATCHER.search):
    """Returns the mp3 file name from the link href"""
    result = test(href)
    return result.groups()[0] if result else ""


def show_hrefs(url):
    """Gets all the hrefs to the show pages"""
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    return (x.get("href") for x in soup.find_all(href=is_show_href))


def mp3_href(base_url, show_href):
    """Finds the href to the mp3 download link for a show page"""
    click.echo(f'Looking for mp3: {show_href}')
    response = requests.get(
        base_url.replace("/all", show_href.replace("/episodes", ""))
    )
    soup = bs(response.text, "html.parser")
    links = (anchor.get("href") for anchor in soup.find_all("a"))
    href = first_true(links, default="", pred=ends_in_mp3)
    click.echo(f'Found mp3: {href}')
    if href.startswith("/"):
        href = base_url.replace("/episodes/all", href)
    return href


def download_if_missing(local_remote):
    """Downloads a remote file if no local copy exists"""
    local, remote = local_remote
    if os.path.exists(local):
        click.echo(f"{local} already exists")
        return
    click.echo(f"Downloading {remote} to {local}")
    write_mp3(download(remote), local)
    click.echo(f"Downloaded {remote} to {local}")


@click.command()
@click.option('-u', '--url', default='https://talkpython.fm/episodes/all',
              help="URL to the episodes list page")
def podcast(url):
    """Finds all the show pages and downloads any missing mp3s"""

    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)

    url_finder = functools.partial(mp3_href, url)

    shows = show_hrefs(url)
    remote_mp3s = pool.map(url_finder, shows)

    local_mp3s = (mp3_name(remote) for remote in remote_mp3s)
    combined = zip(local_mp3s, remote_mp3s)
    pool.map(download_if_missing, combined)
