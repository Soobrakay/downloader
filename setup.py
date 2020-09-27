from setuptools import setup

setup(
    name="downloader",
    version="0.2.0",
    description="Downloads pn or talkpython files",
    long_description="Downloads pn or talkpython.",
    url="http://github.com/Soobrakay",
    author="soobrakay",
    author_email="Soobrakay@users.noreply.github.com",
    license="MIT",
    py_modules=["pn", "talkpython"],
    install_requires=["beautifulsoup4", "more-itertools", "requests"],
    entry_points={"console_scripts": ["pn=pn:crawl", "talkpython=talkpython:crawl"]},
    include_package_data=True,
    zip_safe=False,
)
