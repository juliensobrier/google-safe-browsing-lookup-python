# Copyright 2011 Julien Sobrier
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

""" Version 0.1.0

Google Safe Browsing Lookup library for Python.

If you need to check less than 10,000 URLs a day against the Google Safe Browsing v2 API (http://code.google.com/apis/safebrowsing/), you can use the Lookup API (http://code.google.com/apis/safebrowsing/lookup_guide.html) as a lighter alternative to the more complex API (http://code.google.com/apis/safebrowsing/developers_guide_v2.html).

You need to get an API key from Google at http://code.google.com/apis/safebrowsing/key_signup.html """


import urllib
import urllib2
import re
import httplib


class SafebrowsinglookupClient(object):
    def __init__(self, key='', debug=0, error=0):
        """ Create a new client. You must pass your Google API key (http://code.google.com/apis/safebrowsing/key_signup.html).

            Arguments:
                key: API key.
                debug: Set to 1 to print debug & error output to the standard output. 0 (disabled) by default.
                error: Set to 1 to print error output to the standard output. 0 (disabled) by default.
        """
        self.key = key
        self.debug = debug
        self.error = error
        self.last_error = ''
        self.version = '0.1'
        self.api_version = '3.0'

        if self.key == '':
            raise ValueError("Missing API key")


    def lookup(self, *urls):
        """ Lookup a list of URLs against the Google Safe Browsing v2 lists.

            Returns a hash <url>: <Gooogle match>. The possible values for <Gooogle match> are: "ok" (no match), "malware", "phishing", "malware,phishing" (match both lists) and "error".

            Arguments:
                urls: List of URLs to lookup. The Lookup API allows only 10,000 URL checks a day. If you need more, use the official Google Safe Browsing v2 API implementation (http://code.google.com/p/google-safe-browsing/downloads/list). Each requests must contain 500 URLs at most. The lookup() method will split the list of URLS in blocks of 500 URLs if needed.
        """
        results = {}
        count = 0
        while count * 500 < len(urls):
            inputs = urls[count * 500 : (count + 1) * 500]
            body = len(inputs)

            for url in inputs:
                body = str(body) + "\n" + self.__canonical(str(url))

            self.__debug("BODY:\n" + body + "\n\n")
            url = 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=%s&apikey=%s&appver=%s&pver=%s' % ('python', self.key, self.version, self.api_version)
            self.__debug("URL: %s" % (url))

            response = ''
            try:
                response = urllib2.urlopen(url, body)

                self.__debug("At least 1 match\n")
                results.update( self.__parse(response.read().strip(), inputs) )

            except Exception, e:
                if hasattr(e, 'code') and e.code == httplib.NO_CONTENT: # 204
                    self.__debug("No match\n")
                    results.update( self.__ok(inputs) )

                elif hasattr(e, 'code') and e.code == httplib.BAD_REQUEST: # 400
                    self.__error("Invalid request")
                    results.update( self.__errors(inputs) )

                elif hasattr(e, 'code') and e.code == httplib.UNAUTHORIZED: # 401
                    self.__error("Invalid API key")
                    results.update( self.__errors(inputs) )

                elif hasattr(e, 'code') and e.code == httplib.FORBIDDEN: # 403 (should be 401)
                    self.__error("Invalid API key")
                    results.update( self.__errors(inputs) )

                elif hasattr(e, 'code') and e.code == httplib.SERVICE_UNAVAILABLE: # 503
                    self.__error("Server error, client may have sent too many requests")
                    results.update( self.__errors(inputs) )

                else:
                    self.__error("Unexpected server response")
                    self.__debug(e)
                    results.update( self.__errors(inputs) )


            count = count + 1

        return results



    # Private methods

    # Not much is actually done, full URL canonicalization is not required with the Lookup library according to the API documentation
    def __canonical(self, url=''):
        # remove leading/ending white spaces
        url = url.strip()

        # Remove any embedded tabs and CR/LF characters which aren't escaped.
        url = url.replace('\t', '').replace('\r', '').replace('\n', '')

        # make sure whe have a scheme
        scheme = re.compile("https?\:\/\/", re.IGNORECASE)
        if scheme.match(url) is None:
            url = "http://" + url

        return url


    def __parse(self, response, urls):
        lines = response.splitlines()

        if (len(urls) != len(lines)):
            self.__error("Number of URLs in the response does not match the number of URLs in the request");
            self.__debug( str(len(urls)) + " / " + str(len(lines)) )
            self.__debug(response);
            return self.__errors(urls);


        results = { }
        for i in range(0, len(lines)):
            results.update({urls[i] : lines[i]})

        return results


    def __errors(self, urls):
        results = {}
        for url in urls:
            results.update({url: 'error'})

        return results


    def __ok(self, urls):
        results = {}
        for url in urls:
            results.update({url: 'ok'})

        return results


    def __debug(self, message=''):
        if self.debug == 1:
            print message


    def __error(self, message=''):
        if self.debug == 1 or self.error == 1:
            print message + "\n"
            self.last_error = message
