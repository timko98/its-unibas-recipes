#!/usr/bin/env python
"""PyCharm URL Provider."""
# Copyright (c) 2015-present, Facebook, Inc.
# Modifications copyright 2018 IT Services University Basel
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from __future__ import absolute_import

from xml.dom import minidom

from autopkglib import Processor, ProcessorError

try:
    from urllib.request import urlopen  # For Python 3
except ImportError:
    from urllib2 import urlopen  # For Python 2

__all__ = ["PyCharmURLProvider"]

pyCharm_version_url = 'https://www.jetbrains.com/updates/updates.xml'


class PyCharmURLProvider(Processor):
    """Provide URL for latest PyCharm IDEA build."""

    description = "Provides URL and version for the latest release of PyCharm."
    input_variables = {
        "base_url": {
            "required": False,
            "description": ('Default is '
                            'https://www.jetbrains.com/updates/updates.xml'),
        },
        "edition": {
            "required": False,
            "description": ('Either "community" for "community" or "professional" for "professional" '
                            'edition. Defaults to "community".')
        }
    }
    output_variables = {
        "url": {
            "description": "URL to the latest release of PyCharm",
        }
    }

    __doc__ = description

    def get_pycharm_version(self, intellij_version_url):
        """Retrieve version number from XML."""
        # Read XML
        try:
            f = urlopen(intellij_version_url)
            html = f.read()
            f.close()
        except BaseException as e:
            raise ProcessorError(
                'Can not download %s: %s' % (
                    intellij_version_url, e)
            )

        root = minidom.parseString(html)
        # Get all products in the XML
        products = root.childNodes[0].getElementsByTagName('product')

        intellij_product = None
        for product in products:
            if product.hasAttribute('name') and product.getAttribute('name') == 'PyCharm':
                intellij_product = product

        if intellij_product is not None:
            channels = intellij_product.getElementsByTagName('channel')
            for channel in channels:
                if channel.hasAttribute('licensing') and channel.getAttribute(
                        'licensing') == 'release':
                    if channel.hasAttribute('name') and 'EAP' not in channel.getAttribute('name'):
                        builds = channel.getElementsByTagName('build')
                        available_versions = list()
                        for build in builds:
                            if build.hasAttribute('version'):
                                available_versions.append(build.getAttribute('version'))
                        available_versions.sort(reverse=True)
                        # We can return here because we found the release channel.
                        return str(available_versions[0])
        else:
            raise ProcessorError(
                'Did not find Intellij in version XML.'
            )

    def main(self):
        """Main function."""
        # Determine values.
        version_url = self.env.get('version_url', pyCharm_version_url)
        version = self.get_pycharm_version(version_url)
        download_url = (
                "https://download.jetbrains.com/python/pycharm-%s-%s.dmg" % (
            self.env.get('edition', 'community'), version)
        )

        self.env["url"] = download_url
        self.output("URL: %s" % self.env["url"])


if __name__ == '__main__':
    processor = PyCharmURLProvider()
    processor.execute_shell()
