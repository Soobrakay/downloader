Downloader
==========

Downloader is a simple CLI to download the 2013 workout PDFs from Precision
Nutrition or MP3 files of TalkPython.fm or PythonBytes.fm podcasts.

Installation
------------

Clone the repository, build the distribution, and pipx install.

```shell
git clone https://github.com/soobrakay/downloader.git
cd downloader
python setup.py sdist
pipx install dist/downloader*.tar.gz
```

Usage
-----
Execute downloader with `--help` to see the subcommands. Each subcommand
supports `--help` as well.

```shell
downloader --help
downloader precision-nutrition --help
downloader podcast --help
```
