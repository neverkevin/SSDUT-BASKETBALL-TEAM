#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
from http.GAHTTPHandler import GAHTTPHandler

reload(sys)
sys.setdefaultencoding('utf8')


class NeteaseCrawler():
    def __init__(self):
        self.httpHandler = GAHTTPHandler()
        self.base_url = "http://music.163.com/api/search/get"
        self.detail_url = "http://music.163.com/api/song/detail"
        self.httpHandler.userAgent = u'网易云音乐 1.4.0 (iPhone; iPhone OS 7.0.3; zh_CN)'
        self.httpHandler.headers = {
            "cookie": "MUSIC_U=20898a9f1abd47a387e7bd18f3ccfae31ff06961788bfc4c8357c5dcd60f55665203fd25fe9680afdd9ffd16c0e2dc67a8969285f68b506e; os=iPhone OS; osver=7.0.3; appver=1.7.1; deviceId=b9f815d7c3f9ed4d3c54457ff07fca66"
        }
        self.retryTime = 0
        self.maxRetryTime = 10
        self.fromBeginning = True
        self.songcnt = 0
        self.mvcnt = 0

    def query(self, req):
        return self.query_song(req)

    def query_song(self, req):
        post = {
            "type": 1,
            "sub": "false",
            "s": req,
            "match": "false",
            "limit": 20,
            "offset": 0
        }
        data = self.httpHandler.fetch(self.base_url, post=post)
        api_data = json.loads(data['data'])
        song_list = api_data.get("result", {}).get("songs", [])
        if not song_list:
            return []
        limit = min(5, len(song_list))
        results = []
        for i in xrange(limit):
            song_data = song_list[i]
            song_id = song_data["id"]
            result = self.query_song_by_id(song_id)
            results.extend(result)
        return results

    def query_song_by_id(self, song_id):
        result = self.httpHandler.fetch(
            self.detail_url, get={"ids": "[%s]" % song_id}
            )
        api_result = result.get("data", {})
        api_result = json.loads(api_result)
        if not api_result:
            return []
        return self.__normalize(api_result)

    def __normalize(self, data):
        song_info = data.get("songs")[0]
        mp3_url = song_info["mp3Url"].replace(' ', '')
        song_list = {'0': mp3_url}
        if song_info['mp3Url']:
            result = [{
                "title": song_info.get("name", ''),
                "artist": song_info["artists"][0].get("name", ''),
                "album": song_info["album"].get("name", ''),
                "mp3_url": song_info["mp3Url"],
                "cover_url": song_info["album"].get("picUrl", '')
            }]
        return result
