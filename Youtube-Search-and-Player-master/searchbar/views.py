from types import new_class
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import requests
import re
from isodate import parse_duration
from datetime import datetime
# from searchbar.forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings



search_url = 'https://www.googleapis.com/youtube/v3/search'
video_url = 'https://www.googleapis.com/youtube/v3/videos'


def videodata(request):

    required_data = []

    if request.method == "POST":
        if request.POST['searchbar'] == '':
            messages.error(request, 'Please type something.')
        else:
            search_parameters = {
                'key': settings.YOUTUBE_API_KEY,
                'part': 'snippet',
                'q':request.POST['searchbar'],
                'type':'video',
                'videoEmbeddable': True,
                'maxResults':50,
            }

            fetched_data = requests.get(search_url, params=search_parameters).json()['items']
            
            video_id_list = []
            for data in fetched_data:
                video_id_list.append(data['id']['videoId'])
            
            video_parameters = {
                'key': settings.YOUTUBE_API_KEY,
                'part':'snippet,contentDetails,statistics',
                'id': ','.join(video_id_list),
            }

            video_data = requests.get(video_url, params=video_parameters).json()['items']

            for i in range(search_parameters['maxResults']):
                views = formatted_views(video_data[i]['statistics']['viewCount'])
                try:
                    thumbnail = video_data[i]['snippet']['thumbnails']['standard']['url']
                except KeyError:
                    thumbnail = video_data[i]['snippet']['thumbnails']['high']['url']
                videos = {
                    'id': video_id_list[i],
                    'title': video_data[i]['snippet']['title'],
                    'description': video_data[i]['snippet']['description'],
                    'thumbnail': thumbnail,
                    'duration': str(int(parse_duration(video_data[i]['contentDetails']['duration']).total_seconds()//60))+' mins',
                    'views': views + ' views',
                }
                required_data.append(videos)
            

    return render(request, 'videosearch.html', { 'videos':required_data })

def formatted_views(views):
    views = int(views)
    index = 0
    while views>1000:
        index +=1
        views /= 1000

    if int(views)>=10:
        views = int(views)
        return '%s%s' %(views, ['','K','M','B'][index])
    else:
        return '%.1f%s' % (views, ['','K','M','B'][index])

def player(request, videoid):
    video_parameters = {
        'key': settings.YOUTUBE_API_KEY,
        'part':'snippet,contentDetails,statistics',
        'id': videoid,
    }
    video_data = requests.get(video_url, params=video_parameters).json()['items'][0]
    date = str(video_data['snippet']['publishedAt']).split('T')[0]
    date = datetime.fromisoformat(date)
    month = date.strftime('%b')
    videos = {
        'id':videoid,
        'title': video_data['snippet']['title'],
        'date': f'Uploaded on {month} {date.day}, {date.year}',
        'views': video_data['statistics']['viewCount'] + ' views',
    }
    # srt = YouTubeTranscriptApi.get_transcript(videoid)
    listt = []
    

    def generate_transcript(id):
        transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        

        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                
                script += t + " "
        
        return script, len(script.split())

    id = videoid

    transcript, no_of_words = generate_transcript(id)

       

    
    set_of_words = {}
    
    list = transcript

    set_of_words = set(list.split(' '))
    
    def convert(set):
        return [*set, ]
    
    
    
    s = set(set_of_words)

    aa  = convert(s)

    
    
    for text in aa:
        if ']' not  in text:
            for i in text.split(' '):
                if i not in listt:
                    
                    listt.append(i)










    context = {
        'videos':videos,
        'en':listt,
        # 'numbers':len(),
        #  "uz":uzbek
        }
    

    return render(request, 'videoplayer.html', context )
    


def error_404(request,exception):
    return render(request, '404.html')

def home_1a(request):
    
     return render(request, 'videosearch.html')