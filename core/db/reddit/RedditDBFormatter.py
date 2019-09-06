# -*- coding: utf-8 -*-
from datetime import datetime

from helper.google.GoogleCrawler import GoogleCrawler


class RedditDBFormatter:
    """Allows formatting of RedditChecker Output
    """

    def __init__(self):
        self.seen_subreddits = set()
        self.seen_posts = set()
        self.google_crawler = GoogleCrawler()

    def format_data(self, reddit_data):
        """Corrects the data output format to fit the database

        :param reddit_data: General data from RedditChecker
        :return: Data in a format to be used in DBHandler.insert_to_database
        """
        for data in reddit_data:
            temporary_formatted_data = {}

            if not data.subreddit_id in self.seen_subreddits:
                self.seen_subreddits.add(data.subreddit_id)
                temporary_formatted_data['subreddits'] = self._generate_subreddits_table(data)

            if not data.post_id in self.seen_posts:
                temporary_formatted_data['images'] = self._generate_images_table(data)

                image_url = temporary_formatted_data['images']['image_url']
                temporary_formatted_data['image_processing'] = self._generate_image_processing_table(data, image_url)
                self.seen_posts.add(data.post_id)

            temporary_formatted_data['image_success'] = self._generate_image_success_table(data)
            yield temporary_formatted_data

    def _generate_subreddits_table(self, data):
        return {
            'id': data.subreddit_id,
            'subreddit_name_prefixed': data.subreddit_name_prefixed,
            'subreddit_subscribers': data.subreddit_subscribers,
        }
    
    def _generate_images_table(self, data):
        return {
            'id': data.post_id,
            'subreddit_id': data.subreddit_id,
            'image_url': data.url,
            'permalink': data.permalink,
            'upload_time': data.utc_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        }
    
    def _generate_image_processing_table(self, data, image_url):
        google_process = self.google_crawler.google_reverse_image_search(image_url)
        return {
            'image_id': data.post_id,
            'title': data.title,
            'guess': google_process['guess'],
            'google_permalink': google_process['google_permalink'],
            'first_result': google_process['first_result'],
        }

    def _generate_image_success_table(self, data):
        return {
            'image_id': data.post_id,
            'ups': data.ups,
            'num_comments': data.num_comments,
            'reddit_sort': data.reddit_sort,
            'reddit_time': data.reddit_time,
            'last_checked': datetime.utcnow(),
            'time_passed': str(datetime.utcnow() - data.utc_datetime),
            # TODO generalize
            'gid_1': data.gildings.get('gid_1', None),
            'gid_2': data.gildings.get('gid_2', None),
            'gid_3': data.gildings.get('gid_3', None),
        }
