"""
pn
==

This script will attempt to download the Lean Eating For Men and Lean Eating
For Women workout PDFs from precisionnutrition.com
"""
import click
import multiprocessing
import typing

from . import common

#: Formatter to use for building PDF names.
PDF_FMT = "lef{}-2013-phase-{}.pdf"
#: Location to the s3 bucket where the PDFs are stored.
URL = "https://s3.amazonaws.com/static_web_content/forum_shutdown/members/resources"


def pdf_names(formatter: str = PDF_FMT) -> typing.Iterator[str]:
    """Generates all the valid PDF names for Precision Nutrition 2013 workouts.

    :param formatter: a format string with 2 parameters.
        The first parameter is for gender (m or w).
        The second parameter is for phase (1-12).
    :returns: Generator for all the PDF names for men and women for all 12 phases.
    """
    yield from (
        formatter.format(gender, phase)
        for gender in ("m", "w")
        for phase in range(1, 12)
    )


def local_remotify(pdf_name: str, url: str = URL) -> typing.Tuple[str, str]:
    """Create a tuple of local, remote from a PDF name and URL.

    :param pdf_name: Name of the PDF file to download or local copy name.
    :param url: Remote URL to combine with ``pdf_name`` for remote path.
    :returns: tuple of (local, remote).
        ``local`` is the name of the file on the local system.
        ``remote`` is the URL to the file to download if missing locally.
    """
    return pdf_name, "/".join([url, pdf_name])


@click.command()
def precision_nutrition():
    """Downloads 24 PDFs from Precision Nutrition to the current directory.

    12 PDFs are for designed for men. 12 PDFs are designed for women. The PDFs
    cover 4-6 week periods as phases of the program. Phases are meant to be
    executed in order with later phases containing much harder workouts than
    earlier phases.

    The workouts are designed for specific genders. The major differences
    are the men's workouts are typically 4 strength training days based on an
    upper/lower split and 1 interval day while the women's workouts are 3
    strength training days using an A/B full body workout cycle and 2 interval
    days.
    """
    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
    pool.map(common.download_if_missing, map(local_remotify, pdf_names()))
