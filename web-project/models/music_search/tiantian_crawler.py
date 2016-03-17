# coding=utf8
import json
import random
from urllib import urlencode
from http.GAHTTPHandler import GAHTTPHandler


class TiantianCrawler():
    def __init__(self):
        self.search_url = "http://so.ard.iyyin.com/v2/songs/search"
        self.httpHandler = GAHTTPHandler()
        self.httpHandler.timeout = 10
        self.httpHandler.userAgent = u'tiantian'
        self.uidhash = [
            "0", "1", "2", "3", "4", "5", "6", "7", "8",
            "9", "a", "b", "c", "d", "e", "f"]

    def query(self, req):
        return self.query_song(req)

    def query_song(self, req):
        query = req
        query = urlencode({"q": query})
        uid = self.get_uid()
        api_url = "%s?%s&size=10&page=1&mid=x86_64&v=v3.4.0.2013031220&f=f320&s=s310&splus=9.100000&active=1&net=2&uid=%s" % (self.search_url, query, uid)
        data = self.httpHandler.fetch(api_url)
        data = data.get("data", "{}")
        data = json.loads(data)
        song_list = data.get("data", [])
        if not song_list:
            return []

        limit = min(5, len(song_list))
        results = []
        for i in xrange(limit):
            song_data = song_list[i]
            result = self.normalize(song_data)
            results.extend(result)
        return results

    def get_uid(self):
        ret = ""
        for i in range(0, 32):
            ret += random.choice(self.uidhash)
            if i == 8 or i == 12 or i == 16 or i == 20:
                ret += "-"
        return ret

    def normalize(self, data):
        if data.get('out_list'):
            return []
        if not data.get("url_list"):
            return []
        song_url_list = data.get("url_list")
        sul = song_url_list[len(song_url_list)-1].get('url', '')
        if not sul:
            return []
        result = [{
            "title": data.get("song_name"),
            "artist": data.get("singer_name"),
            "album": data.get("album_name"),
            "mp3_url": sul
            }]
        return result
