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
import requests


def download_data(post, cookies):
    # Set the homepage url
    home_page = "https://piazza.com"
    post_page = "https://piazza.com/class/lz9yd7ft6392yg/post/" + post

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # Start the web browser, load the cookies, the download the required page
    browser = webdriver.Chrome(options=options)

    browser.get(home_page)

    for key in cookies:
        browser.add_cookie({"name":key, "value":cookies[key]})

    browser.get(post_page)
    html = browser.page_source

    # Close browser
    browser.quit()

    return html


def get_cookies(login_info):
    token_page = "https://piazza.com/main/csrf_token"
    login_page = "https://piazza.com/class"

    # login information
    payload = {
        "email":login_info[0],
        "password":login_info[1]
        }

    # create new request session
    session = requests.Session()

    # get request to CSRF token url and parse data
    token = session.get(token_page)
    payload["csrf_token"] = token.text.split('=')[1][1:-2]

    # Extract the required cookies from a login session
    response = session.post(login_page, data=payload)

    if response.status_code == 200:
        print("Successful Login")
    else:
        session.close()
        raise Exception("Error logging in. Response code: "
                    + response.status_code)

    cookies = response.cookies.get_dict()

    # close the session
    session.close()

    return cookies



def get_login():
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    login = [email, password]

    return login