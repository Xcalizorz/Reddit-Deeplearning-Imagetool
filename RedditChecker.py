"""Checks specific subreddit
This modules allows checking specific subreddits and their content
It will connect to the reddit API and provide our tool with
all needed information, such as:

    - Image id
    - Upvotes, downvotes (to check if controversal)
    - Upload timestamp
    - Upload user
    - Amount of comments
    - If removed -> the reason for removal
"""
import requests

from DBHandler import DBHandler
from RedditDownloader import RedditDownloader


# TODO Maybe add PRAW to this
class RedditChecker(RedditDownloader):

    def __init__(self, subreddits):
        """Init for the RedditChecker class
        Allows to add subreddits as a list or str
        :param subreddits: Any amount of subreddit names
            If you use a string, you may seperate subredddits with emptyspaces
            E.g.:
                "memes dankmemes"
        :type subreddits: str, (list, tuple)
        """
        RedditDownloader.__init__(self)

        if isinstance(subreddits, (list, tuple)):
            self.subreddits = subreddits
        else:
            self.subreddits = subreddits.split(" ")

        self.db_handler = DBHandler()

        # TODO Implement as inheritance ?
        # self.reddit_downloader = RedditDownloader()
    @property
    def get_user(self):
        r = requests.get(r'http://www.reddit.com/user/spilcm/comments/.json')
