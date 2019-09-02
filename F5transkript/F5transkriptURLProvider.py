#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import re
from HTMLParser import HTMLParser

from autopkglib import Processor, ProcessorError

try:
    from urllib.request import urlopen  # For Python 3
except ImportError:
    from urllib2 import urlopen  # For Python 2


BASE_URL = "https://www.audiotranskription.de"
REGEX = r'href="(\/audot\/downloadfile\.php\?.*)">Download für Mac \(f5\)'

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
            response = urlopen(BASE_URL + "/downloads.html")
            html_source = response.read()
            escaped_url = re.search(REGEX, html_source).group(1)
            url = HTMLParser().unescape(escaped_url)
            if self.env["verbose"] > 0:
                print("F5transkriptURLProvider: Match found is: %s" % escaped_url)
                print("F5transkriptURLProvider: Unescaped url is: %s" % url)
                print("F5transkriptURLProvider: Returning full url: %s%s" % (BASE_URL, url))
        except BaseException as err:
            raise ProcessorError("Failed to get URL: %s" % err)
        self.env["url"] = BASE_URL + url


if __name__ == "__main__":
    processor = F5transkriptURLProvider()
    processor.execute_shell()
