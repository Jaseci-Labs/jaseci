"""Built in actions for Jaseci"""
from jaseci.jsorc.live_actions import jaseci_action
from fastapi import HTTPException
import base64
import requests
import urllib
import validators


@jaseci_action()
def is_valid(url: str = ""):
    """
    Checks that a string is a valid url in its format
    Param 1 - url string

    Return - True if valid, False if not
    """
    try:
        url_response = validators.url(url)
        if isinstance(url_response, validators.ValidationError):
            return False
    except:
        return False

    return True


@jaseci_action()
def ping(url: str = ""):
    """
    Make sure that a url returns an error code in the 200s when pinged upon success
    Param 1 - url string

    Return - True if error code is in 200s, False if not
    """
    try:
        response = requests.get(url)
    except:
        return False

    return response.status_code in range(200, 299)


@jaseci_action()
def download_text(url: str = ""):
    """
    Downloaded html from a url
    Param 1 - url string

    Return - string containing html
    """
    try:
        response = urllib.request.urlopen(url)
    except:
        raise HTTPException(status_code=404, detail="Invalid URL")

    html_bytes = response.read()
    html_str = html_bytes.decode("UTF-8")
    print(len(html_str))
    return html_str


@jaseci_action()
def download_b64(url: str = ""):
    """
    Downlaod the get response from a url and return it in base64
    Param 1 - url string

    Return - base64 string representing the get response
    """
    try:
        response = requests.get(url)
    except:
        raise HTTPException(status_code=404, detail="Invalid URL")

    response_bytes = response.content
    response_b64_bytes = base64.b64encode(response_bytes)
    response_b64 = response_b64_bytes.decode("ascii")
    return response_b64
