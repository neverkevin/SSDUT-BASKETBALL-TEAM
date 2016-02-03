from tornado import gen
from music_search.netease_crawler import NeteaseCrawler
from music_search.tiantian_crawler import TiantianCrawler


def query(req):
    ne = NeteaseCrawler()
    songs = ne.query(req)
    tt = TiantianCrawler()
    songs.extend(tt.query(req))
    return songs
