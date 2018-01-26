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

import urllib2
import xml.etree.cElementTree as ET

from autopkglib import Processor, ProcessorError


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

  def get_pycharm_version(self, pyCharm_version_url):
    """Retrieve version number from XML."""
    # Read XML
    try:
        req = urllib2.Request(pyCharm_version_url)
        f = urllib2.urlopen(req)
        html = f.read()
        f.close()
    except BaseException as e:
        raise ProcessorError(
          "Can't download %s: %s" % (
            pyCharm_version_url, e)
        )
    # Search for download link.
    root = ET.fromstring(html)
    # root[0][-1] is always the last IDEA release
    build = root[0][-1].find('build')
    version = build.attrib['version']
    # Return pkg url.
    return str(version)

  def main(self):
    """Main function."""
    # Determine values.
    version_url = self.env.get('version_url', pyCharm_version_url)
    version = self.get_pycharm_version(version_url)
    download_url = (
      "https://download.jetbrains.com/python/pycharm-%s-%s.dmg" % (self.env.get('edition', 'community'), version)
    )

    self.env["url"] = download_url
    self.output("URL: %s" % self.env["url"])

if __name__ == '__main__':
    processor = PyCharmURLProvider()
    processor.execute_shell()
