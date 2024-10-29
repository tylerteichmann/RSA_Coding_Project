###############################################################################
#
# Author: Tyler Teichmann
# Date: 2024-10-19
# Purpose: The purpose of this application is to download the Piazza post
# and decode all the encrypted posts.
# Usage: python app.py
#
###############################################################################


from download_html import download_data
from scrape_html import scrape_data


def main():
    # Download data from the piazza web page
    html = download_data("https://piazza.com/class/lz9yd7ft6392yg/post/218")

    # Scrape the Data and reload the page
    scrape_data(html)


if __name__ == "__main__":
    main()