###############################################################################
#
# Author: Tyler Teichmann
# Date: 2024-10-19
# Purpose: This is a support package for the main application. This package is
# responsible for scraping the webpage for the cipher text and replacing it 
# with the plain text message using Beautiful Soup 4.
# Error checking limited at this time.
#
# Referenced Documentation for Beautiful Soup at:
# https://beautiful-soup-4.readthedocs.io/en/latest/#
#
###############################################################################


import re
from bs4 import BeautifulSoup
import rsa


def scrape_data(html):
    # Create initial html parser on passed input
    soup = BeautifulSoup(html, 'html.parser')

    # Select all elements with the followup and row class
    # ignoring those with the comment class
    posts = soup.select(".followup.row:not(.comment)")


    for post in posts:

        # These are all the main threads under the intial posting
        # May be redudant
        response = post.find(
            class_="render-html-content overflow-hidden latex_process"
        )

        # This uses regular expressions to narrow down any content in the
        # intial post to the element that contains the public key removing
        # any white space and converting to a string,
        # i.e. n, e ####, #####    # Public key ...
        #
        # This regular expression is highly spesific and will likely cause
        # issues when posts do not follow the required format.
        key_string = str(
            response.find(
                string=re.compile("^[NnEe] *=? *[0-9]* *[,.]? *[NnEe]")
            )
        ).strip()
        
        try:
            public_key = scrape_public_key(key_string)
        except Exception:
            post_number = post.find(class_="post_number_copy_link")
            print(f"FormattingError: Post {post_number.get_text()} no key found.")
            continue

        # This uses regular expressions to narrow down any content in the
        # intial post to the element that contains the public key removing
        # any white space and converting to a string,
        # i.e. n, e ####, #####    # Public key ...
        #
        # This regular expression is highly spesific and will likely cause
        # issues when posts do not follow the required format.
        message_string = str(
            response.find(
                string=re.compile(re.escape('[') + "[0-9, ]+" + re.escape(']'))
            )
        ).strip()

        ct_message = scrape_ct_message(message_string)

        # For time purposes, only decode messages with n less than 20 digits
        if public_key[0] <= 10000000000000000000:
            try:
                private_key = rsa.break_key(public_key)
            except Exception:
                post_number = post.find(class_="post_number_copy_link")
                print(f"KeyError: Post {post_number.get_text()} no factors of n found.")
                continue
            pt_message = rsa.Decode(private_key, ct_message)
            response.string = pt_message

        # These are all the replies to the main threads
        replies = post.select(
            ".followup_reply .render-html-content.overflow-hidden.latex_process"
        )

        # Itterate over all the replies attempting to decode each
        for reply in replies:

            # Each reply contains only the cypertext so it is much easier to
            # extract the message
            ct_reply_message = (reply
                             .get_text()
                             .strip()
                             .replace("[", "")
                             .replace("]", ""))

            # Try to convert the message to intgers
            # any non-numeric chars will cause a ValueError
            try:
                ct_reply_message = [int(letter) for letter in ct_reply_message.split(',')]
            except ValueError:
                ct_reply_message = str(ct_reply_message)
                reply.string = ct_reply_message
                continue

            # Decode the messages using the public key from that thread
            pt_reply = rsa.Decode(private_key, ct_reply_message)
            reply.string = pt_reply


    # Write all changes to the html document.
    with open("../static/code_breaking.html", "wb") as html:
        html.write(soup.prettify("utf-8"))


# This function scrapes a string that contains the public key
# and returns that meassage as an intger list.
def scrape_public_key(key_string):

    # For loop setup
    length = len(key_string)
    public_key = []
    value = ""
    on_number = False

    # Itterate over every charactre in the string to find two integer values
    # then add them to the public_key as integers
    for i, c in enumerate(key_string):

        if c.isnumeric():
            on_number = True
            value += c
        elif on_number:
            public_key.append(int(value))
            value = ""
            on_number = False

        # if the loop ends on an integer add that integer to the key
        if (i == length - 1) and on_number:
            public_key.append(int(value))
            break

        # Ensure to break if public key is filled, some messages contain
        # many intger values due to sporatic html structure
        if len(public_key) > 1:
            break

    if len(public_key) != 2:
        raise Exceiption
    
    return public_key


# This function scrapes a string that contains the cypher text message
# and returns that meassage as an intger list.
def scrape_ct_message(message_string):

    # For loop setup
    ct_message = ""
    in_message = False

    # Itterate over all characters to find the start of the message
    # then add it to the string until the message is closed
    for i, c in enumerate(message_string):

        if c == '[':
            in_message = True
        elif c == ']':
            in_message = False
            break
        elif in_message:
            ct_message += c


    # try to convert the message to intgers
    # any non-numeric chars will cause a ValueError
    try:
        ct_message = [int(letter) for letter in ct_message.split(',')]
    except ValueError:
        ct_message = str(ct_message)

    return ct_message