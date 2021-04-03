from setuptools import find_packages, setup

setup(
    name="downloader",
    version="0.2.0",
    description="Downloads pn or talkpython files",
    long_description="Downloads pn or talkpython.",
    url="https://github.com/Soobrakay",
    author="soobrakay",
    author_email="Soobrakay@users.noreply.github.com",
    license="MIT",
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=["beautifulsoup4", "click", "more-itertools", "requests"],
    entry_points=dict(console_scripts=["downloader=downloader:cli"]),
    include_package_data=True,
    zip_safe=False,
)
