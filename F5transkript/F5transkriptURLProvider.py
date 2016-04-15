#!/usr/bin/env python

from HTMLParser import HTMLParser
from autopkglib import Processor, ProcessorError

import re
import urllib2


BASE_URL = "https://www.audiotranskription.de"
REGEX = "<a.*?href=\"(.+?)\">f5transkript v3</a>"

__all__ = ["F5transkriptURLProvider"]


class F5transkriptURLProvider(Processor):
    """Provides a download URL for the latest version of F5transkript"""
    description = __doc__
    input_variables = {}
    output_variables = {
        "url": {
            "description": "URL to latest version",
        },
    }

    def main(self):
        try:
            response = urllib2.urlopen(BASE_URL + "/downloads.html")
            html_source = response.read()
            escaped_url = re.search(REGEX, html_source).group(1)
            url = HTMLParser().unescape(escaped_url)
        except BaseException as err:
            raise ProcessorError("Failed to get URL: %s" % err)
        self.env["url"] = BASE_URL + url


if __name__ == "__main__":
    processor = F5transkriptURLProvider()
    processor.execute_shell()
