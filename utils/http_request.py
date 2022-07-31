import urllib.request
from urllib.parse import urlparse


def status(url: str, timeout: int = 30):
    """Checks http reponse status of webpage

    Args:
        url (str): url of webpage
        timeout (int, optional): max time waiting for reponse. Defaults to 30.

    Returns:
        - bool - true if status is successful (200), false otherwise
        - int - http response status code
        - str - url of webpage
    """
    # adds scheme (http protocol) if it is not on url string 
    if not urlparse(url).scheme:
        url = 'http://' + url
    
    # request
    try:
        request = urllib.request.urlopen(url, timeout=timeout)
        http_status_code = request.getcode()
        response_url = request.geturl()
    except urllib.error.URLError:
        http_status_code = 404
        response_url = None

    return http_status_code==200, http_status_code, response_url

