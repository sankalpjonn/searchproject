import requests
import urllib
import json
from multiprocessing import Process, Queue
from requests_oauthlib import OAuth1


class Search():
    def __init__(self, source=None, limit=20):
        # If more search sources need to be added, this dictionary needs to be extended with a new entry
        # url is the address of the source and response_parser is the function used to parse the response of the api into a standard form
        # auth will contain the oauth1 credentails if the api requires it.
        default_sources = {
            "reddit": {
                "url": "https://www.reddit.com/search.json?q={}&limit={}",
                "response_parser": lambda res: [{"text": r['data']['selftext'], "url": r['data']['url']} for r in res['data']['children']] if res else None
            },
            "wikipedia": {
                "url": "https://en.wikipedia.org/w/api.php?action=opensearch&search={}&format=json&limit={}",
                "response_parser": lambda res: [{"text": res[2][i], "url": res[3][i]} for i in range(0, len(res[1]))] if res else None
            },
            "google": {
                "url": "https://www.googleapis.com/customsearch/v1?key=AIzaSyAJOSYS7v_uE95z3kQ_pKyl5p4ONWtTyKg&cx=000720478937699496982:djpylk9bwfm&q={}",
                "response_parser": lambda res: [{"text": item["title"], "url": item["link"]} for item in res['items']] if res and res.get('items') else None
            },
            "duckduckgo": {
                "url": "https://api.duckduckgo.com/?q={}&format=json",
                "response_parser": lambda res: [{"text": item["Text"], "url": item["FirstURL"]} for item in res['RelatedTopics'] if item.get('Text') and item.get('FirstURL')] if res and res.get('RelatedTopics') else None
            },
            "twitter": {
                "url": "https://api.twitter.com/1.1/search/tweets.json?q={}",
                "response_parser": lambda res: [{"text": item["text"], "url": item["entities"]["urls"][0]['url'] if item.get("entities") and item["entities"].get("urls") else None} for item in res['statuses']] if res and res.get('statuses') else None,
                "auth": OAuth1('TyU15xxpc4kcOvd8KevEm7BHF', 'K8eWPZGLdJ7R7zUUO576eU6QHZUeljq6qwtSzYCPlZDTngM98R', '809083502889050112-7Vp2owNANCVe8SdHbVrkzNrVWTM3NxD', '2YdBgwnpOraX3P8obNNe4GXmi92B4JDWexRoVDtn162Sj')
            }
        }
        # by passing the source parameter, the response can be limited to a single source
        self.sources = {source: default_sources[source]} if source else default_sources
        self.q = Queue()
        # it is optional to restrict the search limit of each source by passing the limit parameter. Default will be 20
        self.limit = limit

    def search_data_from_source(self, source, text):
        # format the url with limit and search text and call the api
        res = self.call_source(self.sources[source]['url'].format(text, self.limit), auth=self.sources[source].get("auth"))
        r = self.sources[source]["response_parser"](res)
        # this is an asycnronus method called within an individual process, so put the result in a queue
        self.q.put({source: r[:self.limit]}) if r else self.q.put({source: [{"error": "could not fetch results"}]})

    def run_search(self, text):
        # create a process for searching against each of the source and join them all at the end
        process_list = []
        for source in self.sources.keys():
            p = Process(target=self.search_data_from_source, args=(source, urllib.quote(text)))
            p.start()
            process_list.append(p)
        for p in process_list:
            p.join()
        response = {}
        while not self.q.empty():
            response.update(self.q.get())
        return {"query": text, "results": response}

    def call_source(self, url, auth=None):
        # api call to the source with a timeout of 900 milliseconds
        try:
            r = requests.get(url, timeout=0.9, auth=auth)
            if r.status_code == 200:
                return json.loads(r.text)
            return None
        except:
            return None


if __name__ == "__main__":
    import sys
    s = Search(limit=50)
    re = s.run_search(sys.argv[1])
    print json.dumps(re, indent=4, sort_keys=True)
