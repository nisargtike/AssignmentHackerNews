from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from HackerNewsApp.models import *
from HackerNewsApp.utils import *

from django.shortcuts import render, HttpResponse, get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

import requests
import json

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


def Home(request):
    return render(request, 'HackerNewsApp/home.html')


class FetchTopArticlesAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try: 

            # Fetch new HackerNews IDs 
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            r = requests.get(url=url)
            hackernews_data = json.loads(r.content)
            hackernews_data = hackernews_data[:5]
            # For each hackernews_id check if data exists in our database
            # If data does not exist, create a new object
            for hackernews_id in hackernews_data:
                print("finding ", hackernews_id)
                if Article.objects.filter(hackernews_id=hackernews_id).exists()==False:
                    create_article(hackernews_id)

            # Build response
            response["hackernews_data"] = []
            for hackernews_id in hackernews_data:
                try:
                    article = Article.objects.get(hackernews_id=hackernews_id)
                    temp_data = {}
                    temp_data["hackernews_id"] = article.hackernews_id
                    temp_data["title"] = article.title
                    temp_data["url"] = article.url
                    temp_data["user"] = article.user
                    temp_data["upvotes"] = article.upvotes
                    temp_data["sentiment"] = article.sentiment
                    temp_data["sentiment_score"] = article.sentiment_score
                    response["hackernews_data"].append(temp_data)
                except Exception as e:
                    print("Error with hackernews_id=", hackernews_id, str(e))

            response['status'] = 200

        except Exception as e:
            print("Error FetchTopArticlesAPI", str(e))

        return Response(data=response)


class SearchAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data
            query = data["query"].lower()

            articles = Article.objects.all()

            response["hackernews_data"] = []
            for article in articles:
                text = article.title.lower()
                if query in text:
                    # Build response
                    try:
                        temp_data = {}
                        temp_data["hackernews_id"] = article.hackernews_id
                        temp_data["title"] = article.title
                        temp_data["url"] = article.url
                        temp_data["user"] = article.user
                        temp_data["upvotes"] = article.upvotes
                        temp_data["sentiment"] = article.sentiment
                        temp_data["sentiment_score"] = article.sentiment_score
                        response["hackernews_data"].append(temp_data)
                    except Exception as e:
                        print("Error with hackernews_id=", hackernews_id, str(e))
                    

            response['status'] = 200

        except Exception as e:
            print("Error SearchAPI", str(e))

        return Response(data=response)


FetchTopArticles = FetchTopArticlesAPI.as_view()

Search = SearchAPI.as_view()