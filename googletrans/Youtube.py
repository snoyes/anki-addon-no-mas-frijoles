
from googleapiclient.discovery import build
import re
import urllib.parse as urlparse
import json

with open(r"config.json") as c:
    alljson = c.read()

config = json.loads(alljson)




class YoutubeVideo:
    API = config["API KEY"]

    youtube = build('youtube', 'v3', developerKey=API)


    def __init__(self,link=None,id=None):
        self.link = link
        self.id = id


    @property
    def Id(self):
        # Gets the video ID from a regex
        reID = re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)')
        mo = reID.search(self.link)

        return (mo.group())



    @property
    def title(self):
        title = self.json["items"][0]["snippet"]["title"]
        return title


    def gen_comm(self):
        # generator: yields comments
        match = self.youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            videoId=self.Id,
        ).execute()
        next_token = None

        while match:
            for item in match["items"]:
                comment = item["snippet"]["topLevelComment"]
                text = comment["snippet"]["textOriginal"]
                yield text
            try:
                match = self.youtube.commentThreads().list(
                part="snippet",
                maxResults=100,
                videoId=self.Id,
                pageToken=next_token
            ).execute()
                next_token = match["nextPageToken"]
            except:
                break

    @property
    def json(self):
        #raw json
        req = self.youtube.videos().list(part="snippet",id=self.Id)
        res = req.execute()
        return res

    def __str__(self):
        return "Video number {}: {}".format(self.Id,self.title)



class YoutubeChannel:
    API = config["API KEY"]
    youtube = build('youtube', 'v3', developerKey=API)

    def __init__(self,link):
        self.link = link

    @property
    def channelId(self):
        channelRE = re.compile("channel/(.*)")
        mo = channelRE.search(self.link)
        if mo == None:
            userId = re.compile("user/(.*)")
            mo1 = userId.search(self.link)
            mylist = []
            mylist.append(mo1.group(1))
            return mylist

        return mo.group(1)

    @property
    def all_json(self):
        if type(self.channelId) == type(list()):
            res = self.youtube.channels().list(forUsername=self.channelId, part='contentDetails').execute()
        else:
            res = self.youtube.channels().list(id = self.channelId,part = 'contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None
        while True:
            res = self.youtube.playlistItems().list(playlistId=playlist_id
                                   , part='snippet'
                                   , maxResults=50
                                   , pageToken=next_page_token).execute()

            yield res['items']
            next_page_token = res.get('nextPageToken')

            if next_page_token is None:
                break

    @property
    def all_videos(self):
        for i in self.all_json:
            for every in i:
                yield every['snippet']['resourceId']['videoId']


class YoutubePlaylist:
    API = config["API KEY"]
    youtube = build('youtube', 'v3', developerKey=API)
    '''
    Attributes:
        allId
        VideoId
        title
        comments
        replies
    '''

    def __init__(self,link):
        self.link = link

    @property
    def playlist_id(self):
        url_data = urlparse.urlparse(self.link)
        query = urlparse.parse_qs(url_data.query)
        playlistId = query["list"][0]
        return playlistId

    @property
    def playlist_all_json(self):
        next_page_token = None
        while True:
            res = self.youtube.playlistItems().list(playlistId=self.playlist_id
                                   , part='snippet'
                                   , maxResults=50
                                   , pageToken=next_page_token).execute()

            yield res['items']
            next_page_token = res.get('nextPageToken')

            if next_page_token is None:
                break
    @property
    def playlist_vids(self):
        for i in self.playlist_all_json:
            for every in i:
                yield every['snippet']['resourceId']['videoId']


