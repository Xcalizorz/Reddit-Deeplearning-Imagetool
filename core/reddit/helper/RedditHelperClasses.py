from collections import namedtuple


reddit_data_parameters = [
    'title',
    'post_id',
    'subreddit_id',
    'subreddit_name_prefixed',
    'subreddit_subscribers',
    'ups',
    'gildings',
    'num_comments',
    'reddit_sort',
    'reddit_time',
    'domain',
    'url',
    'permalink',
    'utc_datetime',
]
RedditDataHolder = namedtuple('RedditData', reddit_data_parameters)
