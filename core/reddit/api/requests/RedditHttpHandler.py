import requests


class RedditHttpHandler:
    def __init__(self, headers={'User-agent': 'Test Bot'}):
        self.headers = headers

    def get_response(self, request_query):
        """HTTP Response getter
        Uses 'user-agent': 'Test Bot'
        :param request_query:
            Your request_query
        :type request_query: str
        :return:
            A HTTP response using the request_query
        """
        try:
            return requests.get(request_query, headers=self.headers)
        except ConnectionError as max_retries_exceeded_error:
            print(max_retries_exceeded_error)
            return None

    @staticmethod
    def _create_request_query(sorts_with_timeconditon, subreddit, reddit_sort, reddit_time):
        """Generates a specified request query

        :param sorts_with_timeconditon: A list of sorts with time conditions
        :type sorts_with_timeconditon: list, tuple 
        :param subreddit: The subreddit name
        :type subreddit: str
        :param reddit_sort: Sorting method
        :param reddit_time: Time sorting method
        :return: A specified request query which can be use within requests.get()
        :rtype: str
        """

        if reddit_sort in sorts_with_timeconditon:
            request_query = r'https://www.reddit.com/r/{}/{}/.json?sort={}&t={}'.format(
                subreddit, reddit_sort, reddit_sort, reddit_time
            )
            return request_query

        request_query = r'https://www.reddit.com/r/{}/{}/.json'.format(
            subreddit, reddit_sort
        )
        return request_query
    