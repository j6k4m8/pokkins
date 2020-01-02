import urllib


def get_global_ip() -> str:
    """
    Return the global IP of this machine.
    """
    return urllib.request.urlopen("https://icanhazip.com").read().decode().strip()
