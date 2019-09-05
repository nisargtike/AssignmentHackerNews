from HackerNewsApp.models import *
import requests
import json


def fetch_sentiment_data(text):
    try:
        url = "https://api.aylien.com/api/v1/sentiment"
        data = {
            "text": text
        }

        APPLICATION_ID = "007d1ce1"
        APPLICATION_KEY = "7e9711679f29af3ae7c0db1fde252d95"

        headers = {
            "Accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
            "X-AYLIEN-TextAPI-Application-ID": APPLICATION_ID,
            "X-AYLIEN-TextAPI-Application-Key": APPLICATION_KEY
        }
        print("sentiment_api called")
        r = requests.post(url=url, data=data, headers=headers)
        response = json.loads(r.content)
        return response
    except Exception as e:
        print("Error fetch_sentiment_data")
        response = {}
        response["polarity"] = "Neutral"
        response["polarity_confidence"] = 0
        return response


#response = {u'polarity': u'positive', u'text': u'Arjun is a good football player', u'polarity_confidence': 0.8184565305709839, u'subjectivity_confidence': 0.9611208742121037, u'subjectivity': u'objective'}

def create_article(hackernews_id):
    try:
        url = "https://hacker-news.firebaseio.com/v0/item/" + \
            str(hackernews_id) + ".json"
        r = requests.get(url=url)
        response = json.loads(r.content)

        sentiment_data = fetch_sentiment_data(response["title"])

        Article.objects.create(hackernews_id=hackernews_id,
                               title=response["title"],
                               url=response["url"],
                               user=response["by"],
                               upvotes=response["score"],
                               sentiment=sentiment_data["polarity"],
                               sentiment_score=sentiment_data["polarity_confidence"])
    except Exception as e:
        print("Error create_article ", str(e))


# 20883312
