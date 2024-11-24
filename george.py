# Copyright (c) 2014, Chris DeVisser
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import html.parser, sys, urllib.parse, urllib.request

#Used to parse response text and look for the feedback
class FeedbackHTMLParser(html.parser.HTMLParser):
    isLookingForTextareaTag = False
    isLookingForTextareaData = False
    foundFeedback = False

    #Start looking for textarea content once "Feedback:" has been found
    def handle_starttag(self, tag, attrs):
        if self.isLookingForTextareaTag and tag == 'textarea':
            self.isLookingForTextareaData = True
            self.isLookingForTextareaTag = False

    def handle_endtag(self, tag):
        pass

    #Look for "Feedback:" first and then for the textarea content once the start tag for it has been found
    def handle_data(self, data):
        if 'Feedback:' in data:
            self.isLookingForTextareaTag = True

        if self.isLookingForTextareaData:
            print(data)
            self.foundFeedback = True
            self.isLookingForTextareaData = False


#There should be one command line argument: the .grg file
if len(sys.argv) != 2:
    print('Missing file argument.')
    sys.exit(0)

fileArg = sys.argv[1]

#Read the file
try:
    with open(fileArg, 'r') as file:
        text = file.read()
except:
    print('Problem reading file.')
    sys.exit(0)

#Post the file contents to George as the input script
try:
    url = 'https://student.cs.uwaterloo.ca/~se212/george/ask-george/cgi-bin/george.cgi/check'
    d = text.strip().encode()
    req = urllib.request.Request(url, data=d, headers = {'Content-Type': 'text/plain'}, method='POST')
    resp = urllib.request.urlopen(req)
    george_response = resp.read().decode()
    print(george_response)
except Exception as e:
    print('Problem getting George feedback: ', e)
    sys.exit(0)

