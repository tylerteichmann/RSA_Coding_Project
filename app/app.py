###############################################################################
#
# Author: Tyler Teichmann
# Date: 2024-10-19
# Purpose: The purpose of this application is to download the Piazza post
# and decode all the encrypted posts.
# Usage: python app.py
#
###############################################################################


from download_html import download_data, get_login, get_cookies
from scrape_html import scrape_data


def main():
    post = "218"

    # get login information from user
    login_info = get_login()

    try:
        cookies = get_cookies(login_info)
    except Exception:
        return 201

    # Download data from the piazza web page
    html = download_data(post, cookies)

    # Scrape the Data and reload the page
    scrape_data(html)


if __name__ == "__main__":
    main()