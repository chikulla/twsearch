import datetime


class Tweet:
    def __init__(self, tweetid, screenname, name, timestamp, message):
        self.tweetid = tweetid
        self.screenname = screenname
        self.name = name
        if timestamp:
            self.time = str(datetime.datetime.fromtimestamp(int(timestamp)))
        else:
            self.time = ""
        self.message = message

    def to_str(self):
        msg = self.message.replace('\n', '')
        return self.time + "\t@" + self.dispscreenname() + "\t" + msg

    def dispscreenname(self):
        return self.screenname.ljust(15)
