# -*- coding: utf-8 -*-
"""Checks specific subreddits
This modules allows checking specific subreddits and their content
It will connect to the reddit .json API and provide the tool with
all needed information, such as:

    - Image id
    - Upvotes, downvotes (to check if controversal)
    - Upload timestamp
    - Upload user
    - Amount of comments
    - etc.
"""
from datetime import datetime
from difflib import SequenceMatcher

import requests

from DBHandler import DBHandler
from RedditDBFormatter import RedditDBFormatter
from RedditDownloader import RedditDownloader


class RedditChecker(RedditDownloader):
    """
    RedditChecker allows to check subreddits and filter the json dump if them

    :param RedditDownloader:
        It inherits from the RedditDownloader, which can download
        files from the subreddits specified
    """
    def __init__(self, subreddits, db_file_path='AUTOGENERATED.db', db_type='sqlite3'):
        """Init for the RedditChecker class
        Allows to add subreddits as a list or str
        :param subreddits: Any amount of subreddit names
            If you use a string, you may separate subreddits with emptyspaces
            E.g.:
                "memes dankmemes"
        :type subreddits: str | (list, tuple)

        :param db_file_path:
            The path and name of your database file
        :param db_type:
            The type of your database, defaults to 'sqlite3'
        """
        RedditDownloader.__init__(self)

        if isinstance(subreddits, (list, tuple)):
            self.subreddits = subreddits
        else:
            self.subreddits = subreddits.split(" ")

        self.wrong_subreddit_set = set()
        self.db_handler = DBHandler(db_file_path, db_type)
        self.sorts_with_timeconditon = ('controversial', 'top')
        self.seen_spelling_mistakes = {}

        self.accepted_sorts = {
            'controversial': 1,
            'hot': 2,
            'new': 3,
            'rising': 4,
            'top': 5,
        }

        self.accepted_times = {
            'hour': 1,
            'day': 2,
            'week': 3,
            'month': 4,
            'year': 5,
            'all': 6,
        }

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
        reddit_formatter = RedditDBFormatter()

        json_data_with_sort = self._generate_reddit_json(reddit_sort, reddit_time)
        filtered_data = self._generate_filtered_data_from_json(json_data_with_sort)

        return reddit_formatter.format_data(filtered_data)

    def _generate_filtered_data_from_json(self, json_data):
        """Filters the json output for our needs

        :param json_data:
            Json output from _generate_reddit_json
        """
        for post_data, reddit_sort, reddit_time in json_data:
            for child in post_data:
                child_attributes = child['data']
                child_attributes_data = self._get_child_info(
                    child_attributes, reddit_sort, reddit_time, source_type='image'
                )

                if child_attributes_data:
                    yield child_attributes_data

    def _generate_reddit_json(self, reddit_sort, reddit_time):
        """A generator for the reddit_json api
        Yields the json output of reddit

        :param reddit_sort:
            Sorting mechanism
        :param reddit_time:
            The time sorting mechanism
        :raises KeyError:
            If subreddit does not exist
        """

        for subreddit in self.subreddits:
            if subreddit in self.wrong_subreddit_set:
                continue

            request_query = self._create_request_query(
                subreddit, reddit_sort, reddit_time
            )

            try:
                response = self._get_response(request_query)
                if reddit_time not in self.accepted_times.keys() or reddit_sort not in self.accepted_sorts.keys():
                    reddit_time = self._get_correct_spelling(reddit_time, self.accepted_times.keys())
                    reddit_sort = self._get_correct_spelling(reddit_sort, self.accepted_sorts.keys())
                    request_query = self._create_request_query(
                        subreddit, reddit_sort, reddit_time
                    )
                    response = self._get_response(request_query)
                    if not response.ok:
                        raise KeyError

                print(f'r/{subreddit}/{reddit_sort}/?t={reddit_time}')
                yield response.json()['data']['children'], reddit_sort, reddit_time
            except KeyError:
                self.wrong_subreddit_set.add(subreddit)
                print(f"\tr/{subreddit} does not exists")
                continue

    def _get_correct_spelling(self, reddit_sort_info, accepted_sort_method):
        """Correct spelling
        Checks spelling and replaces the words
        which have been spelled wrong with the word that is
        closes to it in allowed sorting or allowed timing

        :param reddit_sort_info:
            The sorting/timing method given by the user
        :param accepted_sort_method:
            A list of allowed keywords
        :return:
            They correct sort keyword
        """
        if reddit_sort_info in accepted_sort_method:
            return reddit_sort_info
        if reddit_sort_info in self.seen_spelling_mistakes:
            return self.seen_spelling_mistakes[reddit_sort_info]

        best_difference = 0
        self.seen_spelling_mistakes[reddit_sort_info] = None

        for accepted_sort in accepted_sort_method:
            sort_difference = SequenceMatcher(a=reddit_sort_info, b=accepted_sort).ratio()
            # premature stop
            if sort_difference > 0.9:
                temp = accepted_sort
                break
            if sort_difference > best_difference:
                temp = accepted_sort
                best_difference = sort_difference

        print(f"'{temp}' is the correct spelling :)")
        self.seen_spelling_mistakes[reddit_sort_info] = temp
        return temp

    def _get_response(self, request_query):
        """HTTP Response getter
        Uses 'user-agent': 'Test Bot'
        :param request_query:
            Your request_query
        :type request_query: str
        :return:
            A HTTP response using the request_query
        """
        return requests.get(request_query, headers={'User-agent': 'Test Bot'})

    def _create_request_query(self, subreddit, reddit_sort, reddit_time):
        """Generates a specified request query

        :param subreddit: The subreddit name
        :type subreddit: str
        :param reddit_sort: Sorting method
        :param reddit_time: Time sorting method
        :return: A specified request query which can be use within requests.get()
        :rtype: str
        """

        if reddit_sort in self.sorts_with_timeconditon:
            request_query = r'https://www.reddit.com/r/{}/{}/.json?sort={}&t={}'.format(
                subreddit, reddit_sort, reddit_sort, reddit_time
            )
            return request_query

        request_query = r'https://www.reddit.com/r/{}/{}/.json'.format(
            subreddit, reddit_sort
        )
        return request_query

    def _get_child_info(self, child_attributes, reddit_sort, reddit_time, source_type='image'):
        """Gets all data needed for a given source type

        :param child_attributes:
            The children to search through
        :param reddit_sort:
            The sorting method used
        :param reddit_time:
            The time sorting method used
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

        reddit_awards = child_attributes['gildings']
        temp_dict = {
            'title': child_attributes['title'],
            'post_id': child_attributes['id'],
            'subreddit_id': child_attributes['subreddit_id'],
            'upvotes': child_attributes['ups'],
            'comments': child_attributes['num_comments'],
            'reddit_silver': reddit_awards['gid_1'],
            'reddit_gold': reddit_awards['gid_2'],
            'reddit_platinum': reddit_awards['gid_3'],
            'reddit_sort': self.accepted_sorts[reddit_sort],
            'reddit_time': self.accepted_times[reddit_time],
            'subreddit': child_attributes['subreddit_name_prefixed'],
            'subreddit_subscribers': child_attributes['subreddit_subscribers'],
            'domain': child_attributes['domain'],
            'permalink': child_attributes['permalink'],
            'url': child_attributes['url'],
        }

        temp_dict['utc_datetime'] = datetime.utcfromtimestamp(
            child_attributes['created_utc']
        )

        return temp_dict
