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

from core.db.DBHandler import DBHandler
from core.db.reddit.RedditDBFormatter import RedditDBFormatter
from core.reddit.config.RedditConfigrations import reddit_configs
from core.reddit.helper.RedditHelperClasses import RedditDataHolder
from core.reddit.api.requests.RedditHttpHandler import RedditHttpHandler


class RedditChecker:
    """
    RedditChecker allows to check subreddits and filter the json dump of them
    """
    def __init__(self, subreddits, db_file_path, db_type='sqlite3'):
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
        if isinstance(subreddits, (list, tuple)):
            self.subreddits = subreddits
        else:
            self.subreddits = subreddits.split(" ")

        self.seen_spelling_mistakes = {}
        self.wrong_subreddit_set = set()


        self.db_handler = DBHandler(db_file_path, db_type)
        self.reddit_http_handler = RedditHttpHandler()
        self.reddit_db_formatter = RedditDBFormatter()
        self.configs = reddit_configs


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
        json_data_with_sort = self._generate_reddit_json(reddit_sort, reddit_time)
        filtered_data = self._generate_filtered_data_from_json(json_data_with_sort)

        return self.reddit_db_formatter.format_data(filtered_data)

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

            request_query = self.reddit_http_handler._create_request_query(
                self.configs.sorts_with_timeconditon, subreddit, reddit_sort, reddit_time
            )

            try:
                response = self.reddit_http_handler.get_response(request_query)
                if reddit_time not in self.configs.accepted_times.keys() or reddit_sort not in self.configs.accepted_sorts.keys():
                    reddit_time = self._get_correct_spelling(reddit_time, self.configs.accepted_times.keys())
                    reddit_sort = self._get_correct_spelling(reddit_sort, self.configs.accepted_sorts.keys())
                    request_query = self.reddit_http_handler._create_request_query(
                        self.configs.sorts_with_timeconditon, subreddit, reddit_sort, reddit_time
                    )
                    response = self.reddit_http_handler.get_response(request_query)
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
        :return:
            Returns a RedditDataHolder, which is essentially a dict with
            values filtered from te original data returned by Reddits API
        :rtype: RedditDataHolder
        """
        try:
            is_source_type = child_attributes['post_hint'] == source_type
            if not is_source_type:
                return None
        except KeyError:
            if source_type != 'text':
                return None

        return RedditDataHolder(
            title=child_attributes['title'].title(),
            post_id=child_attributes['id'],
            subreddit_id=child_attributes['subreddit_id'],
            subreddit_name_prefixed=child_attributes['subreddit_name_prefixed'],
            subreddit_subscribers=child_attributes['subreddit_subscribers'],
            ups=child_attributes['ups'],
            gildings=child_attributes['gildings'],
            num_comments=child_attributes['num_comments'],
            reddit_sort=self.configs.accepted_sorts[reddit_sort],
            reddit_time=self.configs.accepted_times[reddit_time],
            domain=child_attributes['domain'],
            url=child_attributes['url'],
            permalink=child_attributes['permalink'],
            utc_datetime=datetime.utcfromtimestamp(child_attributes['created_utc']),
        )
