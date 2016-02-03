import urllib2
import urllib
import httplib
from StringIO import StringIO
from GAHTTPErrorHandler import GAHTTPRedirectErrorHandler, \
    GAHTTPDefaultErrorHandler


class GAHTTPHandler:
    USERAGENT = ""
    ContentCache = {}
    TimeCache = {}

    def __init__(self):
        self.enableRedirect = True
        self.userAgent = self.__class__.USERAGENT
        self.referer = ''
        self.enableGZip = True
        self.timeout = 60
        self.headers = {}
        self.url = ''

    def enableDebug(self):
        httplib.HttpConnection.debugLevel = 1

    def __constructURL(self, url, getParam):
        """return the url constructed from url and get parameters"""
        if getParam is not None:
            sep = url.find("?") == -1 and "?" or "&"
            paramString = "&".join(
                ["%s=%s" % (k, v) for k, v in getParam.items()])
            return url + sep + paramString
        else:
            return url

    def open(self, url, postData=None):
        if postData is not None:
            request = urllib2.Request(url, urllib.urlencode(postData))
        else:
            request = urllib2.Request(url)
        request.add_header('User-Agent', self.userAgent)
        if url in self.__class__.TimeCache:
            timeCache = self.__class__.TimeCache[url]
            if 'eTag' in timeCache:
                request.add_header('If-None_Match', timeCache['eTag'])
            if 'last_modified' in timeCache:
                request.add_header(
                    'If-Modified-Since', timeCache['last_modified'])
        if self.enableGZip:
            request.add_header('Accept-Encoding', 'gzip')
        if self.referer and len(self.referer) > 0:
            request.add_header('Referer', self.referer)
        if self.headers:
            for k, v in self.headers.items():
                request.add_header(k, v)
        opener = urllib2.build_opener(
            GAHTTPRedirectErrorHandler(), GAHTTPDefaultErrorHandler()
            )
        return opener.open(request, timeout=self.timeout)

    def fetch(self, url, get=None, post=None):
        self.url = self.__constructURL(url, get)
        sock = self.open(self.url, post)
        result = {}
        # not modified
        if hasattr(sock, 'status') and sock.status == 304:
            result['data'] = self.__class__.ContentCache[url]
        else:
            result['data'] = sock.read()
            timeCache = {}
            if url in self.__class__.TimeCache:
                timeCache = self.__class__.TimeCache[url]
            timeCache['eTag'] = sock.headers.get('ETag')
            timeCache['last_modified'] = sock.headers.get('Last-Modified')
            self.__class__.TimeCache[url] = timeCache
            if sock.headers.get('content-encoding', '') == 'gzip':
                import gzip
                result['data'] = gzip.GzipFile(
                    fileobj=StringIO(result['data'])).read()
            # cache is enabled by server
            if timeCache['eTag'] or timeCache['last_modified']:
                self.__class__.ContentCache[url] = result['data']
            sock.status = 200

        result['status'] = sock.status
        result['url'] = sock.url
        sock.close()
        return result
