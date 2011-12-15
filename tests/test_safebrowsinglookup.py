#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Julien Sobrier
#
# This file is part of printio released under MIT license.
# See the LICENSE for more information.
"""

Test the library.

"""

import os
import sys
import unittest

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not libpath in sys.path:
    sys.path.insert(1, libpath)
del libpath

from safebrowsinglookup import SafebrowsinglookupClient


class SafebrowsinglookupClient_ParseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = SafebrowsinglookupClient('insert_API_key_here')

    def test_errors(self):
        client = SafebrowsinglookupClient('AAAAAAAAaaAAAaAAAaA0a0AaaAAAAAAa0AaAAAaAa0aaaAaAa0Aa0AaaaA')
        results = client.lookup(*['http://www.google.com/', 'http://www.google.org/'])

        self.assertEquals(2, len(results))
        self.assertEquals('error', results['http://www.google.com/'])
        self.assertEquals('error', results['http://www.google.org/'])


    def test_no_match(self):
        if self.client.key == 'insert_API_key_here':
            return

        results = self.client.lookup(*['http://www.google.com/', 'http://www.google.org/'])

        self.assertEquals(2, len(results))
        self.assertEquals('ok', results['http://www.google.com/'])
        self.assertEquals('ok', results['http://www.google.org/'])


    def test_match(self):
        if self.client.key == 'insert_API_key_here':
            return

        results = self.client.lookup('http://www.gumblar.cn/')

        self.assertEquals(1, len(results))
        self.assertEquals('malware', results['http://www.gumblar.cn/'])


    def test_match_many(self):
        if self.client.key == 'insert_API_key_here':
            return

        urls = []
        for i in range(1, 600):
            urls.append("http://www.gumblar.cn/" + str(i))

        results = self.client.lookup(*urls)

        self.assertEquals(len(urls), len(results))
        self.assertEquals('malware', results['http://www.gumblar.cn/1'])
        self.assertEquals('malware', results['http://www.gumblar.cn/500'])
        self.assertEquals('malware', results['http://www.gumblar.cn/599'])




if __name__ == "__main__":
    unittest.main()