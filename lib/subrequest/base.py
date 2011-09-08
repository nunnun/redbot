#!/usr/bin/env python

"""
Subrequests to do things like range requests, content negotiation checks,
and validation.

This is the base class for all subrequests.
"""

__author__ = "Mark Nottingham <mnot@mnot.net>"
__copyright__ = """\
Copyright (c) 2008-2011 Mark Nottingham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from redbot.fetch import RedFetcher


class SubRequest(RedFetcher):
    """
    A subrequest of a "main" ResourceExpertDroid, made to perform additional
    behavioural tests on the resource.
    
    it both adorns the given red's state, and saves its own state in the
    given red's subreqs dict.
    """
    def __init__(self, red, name):
        self.base = red.state
        req_hdrs = self.modify_req_hdrs()
        RedFetcher.__init__(self, self.base.uri, self.base.method, req_hdrs,
                            self.base.req_body, red.status_cb, [], name)
        self.base.subreqs[name] = self.state
    
    def modify_req_hdrs(self):
        """
        Usually overidden; modifies the request's headers.
        
        Make sure it returns a copy of the orignals, not them.
        """
        return list(self.base.orig_req_hdrs)

    def setMessage(self, subject, msg, subreq=None, **kw):
        self.base.setMessage(subject, msg, self.state.type, **kw)