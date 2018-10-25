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


class RedditChecker(RedditDownloader):
    """
    RedditChecker allows to check subreddits and filter the json dump if them

    :param RedditDownloader:
        It inherits from the RedditDownloader, which can download
        files from the subreddits specified
    """
    def __init__(self, subreddits):
        """Init for the RedditChecker class
        Allows to add subreddits as a list or str
        :param subreddits: Any amount of subreddit names
            If you use a string, you may separate subreddits with emptyspaces
            E.g.:
                "memes dankmemes"
        :type subreddits: str | (list, tuple)
        """
        RedditDownloader.__init__(self)

        if isinstance(subreddits, (list, tuple)):
            self.subreddits = subreddits
        else:
            self.subreddits = subreddits.split(" ")

        self.db_handler = DBHandler()

        # TODO Implement as inheritance ?
        # self.reddit_downloader = RedditDownloader()

    def subreddit_data(self, reddit_sort='new', reddit_time='hour'):
        """Generates all needed data, taken via the .json backend of reddit

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
        data = []
        filtered_data = []

        for subreddit in self.subreddits:
            try:
                data.append(
                    requests.get(
                        r'https://www.reddit.com/r/{}/{}/.json?sort={}&t={}'.format(
                            subreddit, reddit_sort, reddit_sort, reddit_time
                        ), headers={'User-agent': 'Test Bot'}
                    ).json()['data']['children']
                )
            except KeyError:
                print(f"'{subreddit}' does not exists")
                continue

        for post_data in data:
            for child in post_data:
                child_attributes = child['data']
                child_attributes_data = self._get_child_info(child_attributes, 'image')

                if child_attributes_data:
                    filtered_data.append(child_attributes_data)

        return filtered_data

    @staticmethod
    def _get_child_info(child_attributes, source_type='image'):
        """Gets all data needed for a given source type

        :param child_attributes:
            The children to search through
        :param source_type:
            The type you want to check
                video
                image
                etc.
        :type source_type: str
        :return: Returns a dictionary of the data
        :rtype: Dict, None if no objects of source_type found
        """
        try:
            is_source_type = child_attributes['post_hint'] == source_type
        except KeyError:
            if not source_type == 'text':
                return None
        if not child_attributes['post_hint'] == source_type:
            return None

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

        temp_dict['utc_datetime'] = datetime.utcfromtimestamp(
            child_attributes['created_utc']
        ).strftime('%Y-%m-%d %H:%M:%S')

        return temp_dict
