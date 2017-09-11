#!/usr/bin/env python3
"""
download_precision_nutrition
============================

This script will attempt to download the Lean Eating For Men and Lean Eating
For Women workout PDFs from precisionnutrition.com

The script requires `requests` to function.
Inside a virtualenv, install with:

```shell
pip install bs4 requests
```

Once those are installed, run the script with:

```shell
python download_precision_nutrition.py
```
"""
import multiprocessing
import os

import requests  # pylint: disable=import-error

URL_FMT = 'https://s3.amazonaws.com/static_web_content/forum_shutdown/members/resources/lef{}-2013-phase-{}.pdf'  # noqa pylint: disable=line-too-long


def write_pdf(content, name):
    """Writes pdf `content` to `name` file"""
    if not content:
        print('no content for ', name)
        return
    with open(name, mode='wb') as pdf_file:
        pdf_file.write(content)


def download(href):
    """Get the content of an mp3 link"""
    response = requests.get(href)
    return response.content if response.ok else ''


def download_if_missing(local_remote):
    """Downloads a remote file if no local copy exists"""
    local, remote = local_remote
    if os.path.exists(local):
        print('{} already exists'.format(local))
        return
    print('Downloading {} to {}'.format(remote, local))
    write_pdf(download(remote), local)
    print('Downloaded {} to {}'.format(remote, local))


def crawl():
    """Tries to guess the PDF names and download them"""
    remote_pdfs = [
        URL_FMT.format(gender, phase)
        for gender in ('m', 'w')
        for phase in range(1, 12)
    ]
    local_pdfs = (x.split('/')[-1] for x in remote_pdfs)
    combined = zip(local_pdfs, remote_pdfs)
    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
    pool.map(download_if_missing, combined)


if __name__ == '__main__':
    crawl()
