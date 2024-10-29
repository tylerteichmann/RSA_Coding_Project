###############################################################################
#
# Author: Tyler Teichmann
# Date: 2024-10-19
# Purpose: This is a support package for the main application. This package is
# responsible for downloading the html using browser automation selenium.
# Ensure all required cookies are located in the cookies.txt file in the format
# name=cookie
#
# Referenced Documentation for Selenium at:
# https://www.selenium.dev/documentation/
#
###############################################################################


from selenium import webdriver


def download_data(url):
    # Set the homepage url
    homepage = url

    # Import the required cookies from the cookies.txt file located in static
    Cookies = []

    with open("../static/cookies.txt", "r") as file:
        for line in file:
            line = line.strip()
            key, value = line.split("=")
            Cookies.append({"name":key, "value":value})

    # Start the web browser, load the cookies, the download the required page
    browser = webdriver.Chrome()

    browser.get(homepage)

    for cookie in Cookies:
        browser.add_cookie(cookie)

    browser.get(url)
    html = browser.page_source

    # Close browser
    browser.close()

    return html