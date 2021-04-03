#!/usr/bin/env python3
"""
download_precision_nutrition
============================

This script will attempt to download the Lean Eating For Men and Lean Eating
For Women workout PDFs from precisionnutrition.com
"""
import click
import multiprocessing
import os

import requests

#: Formatter to use for building PDF names.
PDF_FMT = "lef{}-2013-phase-{}.pdf"
#: Location to the s3 bucket where the PDFs are stored.
URL = "https://s3.amazonaws.com/static_web_content/forum_shutdown/members/resources"


def download(href):
    """Get the content of an mp3 link"""
    response = requests.get(href)
    return response.content if response.ok else ""


def download_if_missing(pdf, url=URL):
    """Downloads a remote file if no local copy exists"""
    if os.path.exists(pdf):
        click.echo(f"{pdf} already exists")
        return
    remote = "/".join([url, pdf])
    click.echo(f"Downloading {remote} to {pdf}")
    content = download(remote)
    if content:
        write_pdf(content, pdf)
        click.echo(f"Downloaded {remote} to {pdf}")
    else:
        click.echo(f"No content: {remote}")


def pdf_names(formatter=PDF_FMT):
    """Generator of PDF names"""
    yield from (
        formatter.format(gender, phase)
        for gender in ("m", "w")
        for phase in range(1, 12)
    )


def write_pdf(content, name):
    """Writes pdf `content` to `name` file"""
    with open(name, mode="wb") as pdf_file:
        pdf_file.write(content)


@click.command()
def precision_nutrition():
    """Tries to guess the PDF names and download them"""
    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
    pool.map(download_if_missing, pdf_names())
