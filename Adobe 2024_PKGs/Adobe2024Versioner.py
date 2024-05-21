#!/usr/local/autopkg/python
# pylint: disable = invalid-name

# Standard Imports
from __future__ import absolute_import
import os
import subprocess
import xml.etree.ElementTree as ET


# AutoPkg imports
# pylint: disable = import-error
from autopkglib import Processor, ProcessorError


# Define class
__all__ = ['Adobe2024Versioner']
__version__ = ['1.4.11']


# Class def
class Adobe2024Versioner(Processor):
    '''
       Parses Adobe 2024 PKG files for version info.
    '''

    description = __doc__

    input_variables = {
        'pkg_path': {
            'required': True,
            'description': 'Path to the Adobe 2024 PKG file.',
        },
    }

    output_variables = {
        'version': {
            'description': 'The version of the Adobe 2024 package.',
        },
    }


    def main(self):
        '''
            Main function to get the version from the PKG file.
        '''

        # Get the PKG file path from the input variable
        pkg_path = self.env['pkg_path']

        # Use xattr to extract the version information from the PKG metadata
        try:
            output = subprocess.check_output(['xattr', '-p', 'com.apple.pkg.metadata.version', pkg_path])
            plist_data = ET.fromstring(output)
            version = plist_data.find('./pkg-version').text
            self.env['version'] = version
            self.output("Version: {}".format(version))
        except (subprocess.CalledProcessError, ET.ParseError) as err_msg:
            raise ProcessorError("Failed to extract version from PKG metadata: {}".format(err_msg))

        # Create pkginfo with found details
        self.create_pkginfo()


    def create_pkginfo(self):
        '''
            Create pkginfo with found details
        '''

        pkginfo = {
            'version': self.env['version'],
        }

        self.env['additional_pkginfo'] = pkginfo
        self.output("additional_pkginfo: {}".format(self.env['additional_pkginfo']))


if __name__ == '__main__':
    PROCESSOR = Adobe2024Versioner()