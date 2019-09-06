from collections import namedtuple

"""Holds the general configurations needed while working with the Reddit api
"""
RedditConfigurations = namedtuple(
    "RedditConfigrations", field_names=["accepted_sorts", "accepted_times", "sorts_with_timeconditon"]
)

__accepted_sorts = {
    'controversial': 1,
    'hot': 2,
    'new': 3,
    'rising': 4,
    'top': 5,
}

__accepted_times = {
        'hour': 1,
        'day': 2,
        'week': 3,
        'month': 4,
        'year': 5,
        'all': 6,
}

__sorts_with_timeconditon = ('controversial', 'top')

reddit_configs = RedditConfigurations(__accepted_sorts, __accepted_times, __sorts_with_timeconditon)