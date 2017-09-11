Downloader
==========

Downloader is a simple python package to download things I wanted to download.

Installation
------------

Clone the repository, build the distribution, and pip install.

```shell
git clone https://github.com/soobrakay/downloader
cd downloader
python setup.py sdist
pip install dist/downloader-0.1.tar.gz
```

Usage
-----

Downloader installs two executables, `pn` and `talkpython`.

`pn` will download Precision Nutrition workout PDFs to the current working
directory.

`talkpython` will download the talkpython.fm podcasts in `mp3` format to the
current working directory.
