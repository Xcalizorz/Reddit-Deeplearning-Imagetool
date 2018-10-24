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
from datetime import datetime
import requests

from DBHandler import DBHandler
from RedditDownloader import RedditDownloader


# TODO Maybe add PRAW to this
class RedditChecker(RedditDownloader):
    """
    RedditChecker allows to check subreddits and filter the json dump if them

    :param RedditDownloader:
        It inherits from the RedditDownloader, which can download
        files from the subreddits specified
    """
    def __init__(self, subreddits, reddit_sort='new', reddit_time='day'):
        """Init for the RedditChecker class
        Allows to add subreddits as a list or str
        :param subreddits: Any amount of subreddit names
            If you use a string, you may separate subreddits with emptyspaces
            E.g.:
                "memes dankmemes"
        :type subreddits: str | (list, tuple)
        :param reddit_sort:
            How to sort the subreddit
                new
                hot
                controversal
                top
                rising
        :param reddit_time:
            Which time spaces to check:
                hour
                day
                week
                month
                year
                all (all time)

        """
        RedditDownloader.__init__(self)

        if isinstance(subreddits, (list, tuple)):
            self.subreddits = subreddits
        else:
            self.subreddits = subreddits.split(" ")

        self.reddit_sort = reddit_sort
        self.reddit_time = reddit_time
        self.db_handler = DBHandler()

        # TODO Implement as inheritance ?
        # self.reddit_downloader = RedditDownloader()
    @property
    def subreddit_data(self):
        """Generates all needed data, taken via the .json backend of reddit

        """
        data = requests.get(
            r'https://www.reddit.com/r/{}/{}/.json?sort={}&t={}'.format(
                self.subreddits[0], self.reddit_sort, self.reddit_sort, self.reddit_time
            ), headers={'User-agent': 'Test Bot'}
        ).json()

        filtered_data = []

        for child in data['data']['children']:
            child_attributes = child['data']

            if child_attributes['post_hint'] == 'image':
                temp_dict = {
                    'id': child_attributes['id'],
                    'upvotes': child_attributes['ups'],
                    'downvotes': child_attributes['downs'],
                    'subreddit': child_attributes['subreddit_name_prefixed'],
                    'subreddit_subscribers': child_attributes['subreddit_subscribers'],
                    'domain': child_attributes['domain'],
                    'permalink': child_attributes['permalink'],
                    'image_url': child_attributes['url'],
                }

                temp_dict['datetime'] = datetime.utcfromtimestamp(
                    child_attributes['created_utc']
                ).strftime('%Y-%m-%d %H:%M:%S') + str(" UTC")

                filtered_data.append(temp_dict)

        return filtered_data
