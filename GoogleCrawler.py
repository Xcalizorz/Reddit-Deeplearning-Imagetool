import re

import requests


class GoogleCrawler:
    def __init__(self):
        self.USER_AGENT = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/json',
        }
        self.google_knows = False

    def google_reverse_image_search(self, image_url):
        """Uses googles reverse image search
        Returns main information as a dictionary

        :param image_url:
            A URL to the image to be analyzed
        :return: 
            - Google Permalink to the search
            - Guess whats on the picture
            - Link of first result
        :rtype: Dict
        """
        google_url = f'https://images.google.com/searchbyimage?image_url={image_url}'
        response = requests.get(google_url, headers=self.USER_AGENT)

        result = {
            'google_permalink': None,
            'guess': None,
            'first_result': None,
        }

        if response.status_code == 503:
            if not self.google_knows:
                print("Google found out you're a bot!\nAuthorize here:\t")
                print(response.url)
                self.google_knows = True
                # search google for title
            return result

        try:
            information = re.search(r'<a class="fKDtNb" href="(.*?)</a>',
                                    response.text).group(1).split('style="font-style:italic">')
            result['google_permalink'] = information[0].replace('"', '')
            result['guess'] = information[1].title()
        except AttributeError:
            pass

        try:
            result['first_result'] = re.search(r'<div class="r"><a href="(.*?)"', response.text).group(1)
        except AttributeError:
            pass

        return result
