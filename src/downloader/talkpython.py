"""
talkpython
==========

This script attempts to find all MP3 links to podcast episodes for
TalkPython.fm or PythonBytes.fm and download any MP3s not available in the
current working directory
"""
import functools
import multiprocessing
import re
import typing

import click
import requests
from bs4 import BeautifulSoup
from more_itertools import first_true

from . import common

#: Regex to find the name of the .mp3 file to download.
MP3_MATCHER = re.compile(r"/([^/]*.mp3)", re.IGNORECASE)


def is_show_href(href: str) -> bool:
    """Returns True for links with hrefs to show pages

    :param href: The href attribute from an anchor tag on the episodes page.
    :returns: True if it looks like a show tag, False otherwise.
    """
    return href and "/episodes/show/" in href.lower()


def ends_in_mp3(href: str) -> bool:
    """True if the link ends in .mp3

    :param href: The href attribute from an anchor tag on a show page.
    :returns: True if it ends in .mp3, False otherwise.
    """
    return href and href.lower().endswith(".mp3")


def mp3_name(
    href: str,
    fn: typing.Callable[[str], typing.Optional[typing.Match]] = MP3_MATCHER.search,
) -> str:
    """MP3 filename from a link or empty string if no filename found.

    :param href: HREF attribute from an anchor tag on a show page.
    :param fn: Test function to find the MP3. Should return re.Match or None
    :returns: MP3 filename or empty string if no filename found.
    """
    match = fn(href)
    return match.groups()[0] if match else ""


def show_hrefs(url: str) -> typing.Iterable[str]:
    """Find all the URLs to episode show pages from the episodes list page.

    :param url: URL to the episodes list page to scan.
    :returns: URLs tot he show pages.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return map(lambda anchor: anchor.get('href'), soup.find_all(href=is_show_href))


def mp3_href(base_url: str, show_href: str) -> str:
    """Finds the href to the mp3 download link for a show page.

    :param base_url: URL to the episodes list page.
    :param show_href: Relative URL to the show page.
    :returns: URL to the MP3 file
    """
    root_url = base_url.replace('/episodes/all', '')
    click.echo(f"Looking for mp3: {show_href}")
    response = requests.get(''.join([root_url, show_href]))
    soup = BeautifulSoup(response.text, "html.parser")
    links = (anchor.get("href") for anchor in soup.find_all("a"))
    href = first_true(links, default="", pred=ends_in_mp3)
    click.echo(f"Found mp3: {href}")
    href = ''.join([root_url, href]) if href.startswith('/') else href
    return href


@click.command()
@click.option(
    "-u",
    "--url",
    default="https://talkpython.fm/episodes/all",
    help="URL to the episodes list page",
)
def podcast(url):
    """Downloads MP3s from TalkPython.fm or PythonBytes.fm to current directory.

    Default URL is https://talkpython.fm/episodes/all and will download all
    episode MP3s to the current directory.

    Use ``--url https://pythonbytes.fm/episodes/all`` to download all episode
    MP3s from PythonBytes.fm instead.
    """

    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)

    shows = show_hrefs(url)

    url_finder = functools.partial(mp3_href, url)
    remote_mp3s = pool.map(url_finder, shows)

    local_mp3s = (mp3_name(remote) for remote in remote_mp3s)
    combined = zip(local_mp3s, remote_mp3s)
    pool.map(common.download_if_missing, combined)
