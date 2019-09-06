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
        result = {
            'google_permalink': None,
            'guess': None,
            'first_result': None,
        }
        if self.google_knows:
            return result

        response = self._request_response(image_url)

        if self._google_blocked_me(response):
            return result

        result.update(self._extract_permalink_guess(response))
        result.update(self._extract_first_result(response))

        return result

    def _extract_first_result(self, response):
        first_result = self._extract_information(
            r'<div class="r"><a href="(.*?)"',
            response.text,
        ).pop()  # splitting by None will generate a list with 1 item

        return {'first_result': first_result}

    def _extract_permalink_guess(self, response):
        result = self._extract_information(
            r'<a class="fKDtNb" href="(.*?)</a>',
            response.text,
            'style="font-style:italic">',
        )
        
        return {
            'google_permalink': result[0].replace('"', ''),
            'guess': result[1].title(),
        }

    def _request_response(self, url):
        google_url = f'https://images.google.com/searchbyimage?image_url={url}'
        return requests.get(google_url, headers=self.USER_AGENT)

    def _extract_information(self, regex, text, split_by=None, group_at=1):
        try:
            return re.search(regex, text).group(group_at).split(split_by)            
        except AttributeError:
            pass

    def _google_blocked_me(self, response):
        if response.status_code == 503:
            if not self.google_knows:
                print("Google found out you're a bot!\nAuthorize here:\t")
                print(response.url)
                self.google_knows = True
        