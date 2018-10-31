# -*- coding: utf-8 -*-
from datetime import datetime


class RedditDBFormatter:
    """Allows formatting of RedditChecker Output
    """

    def __init__(self):
        self.seen_subreddits = set()
        self.seen_posts = set()

    def format_data(self, reddit_data):
        """Corrects the data output format to fit the database

        :param reddit_data: General data from RedditChecker
        :return: Data in a format to be used in DBHandler.insert_to_database
        """

        correct_reddit_data = []
        for data in reddit_data:
            temp = {}

            if not data['subreddit_id'] in self.seen_subreddits:
                subreddit_table = {
                    'id': data['subreddit_id'],
                    'subreddit': data['subreddit'],
                    'subscriber_number': data['subreddit_subscribers'],
                }

                temp['subreddits'] = subreddit_table
                self.seen_subreddits.add(data['subreddit_id'])

            if not data['post_id'] in self.seen_posts:
                images_table = {
                    'id': data['post_id'],
                    'subreddit_id': data['subreddit_id'],
                    'image_url': data['url'],
                    'permalink': data['permalink'],
                    'upload_time': data['utc_datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                }
                temp['images'] = images_table

            image_success_table = {
                'image_id': data['post_id'],
                'upvotes': data['upvotes'],
                'downvotes': data['downvotes'],
                'comments': data['comments'],
                'reddit_gold': data['reddit_gold'],
                'last_checked': datetime.utcnow(),
                'time_passed': str(datetime.utcnow() - data['utc_datetime']),
            }
            temp['image_success'] = image_success_table

            image_processing_table = {
                'image_id': data['post_id'],
                'process_result': "",
            }
            temp['image_processing'] = image_processing_table

            correct_reddit_data.append(temp)

            self.seen_posts.add(data['post_id'])

        return correct_reddit_data
