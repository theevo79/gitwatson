from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EmotionOptions, KeywordsOptions, EntitiesOptions, SentimentOptions
import os, sys
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np

from matplotlib.patches import Circle, Wedge, Rectangle

from .models import News, Ents

# Create your views here.

#apikey = 'pJ-AKe9eWBAv1eTE4nIexYxLgeFBeAVGj7ETGkDNGhPG'
apikey = os.environ.get('IBM_API_KEY', 'pJ-AKe9eWBAv1eTE4nIexYxLgeFBeAVGj7ETGkDNGhPG')
curl = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/1df9908c-b756-4369-a441-d6688dfd6b4b'
authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(curl)



def degree_range(n): 
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

def gauge(labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], \
          colors='jet_r', arrow=1, title='', fname=False): 
    
    """
    some sanity checks first
    'jet_r'
    """
    
    N = len(labels)
    
    # if arrow > N: 
    #     raise Exception("\n\nThe category ({}) is greated than \
    #     the length\nof the labels ({})".format(arrow, N))
 
    
    """
    if colors is a string, we assume it's a matplotlib colormap
    and we discretize in N discrete colors 
    """
    
    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list): 
        if len(colors) == N:
            colors = colors[::-1]
        else: 
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors), N))

    """
    begins the plotting
    """
    
    #fig, ax = plt.subplots()
    fig = Figure()
    ax = fig.subplots()

    ang_range, mid_points = degree_range(N)

    labels = labels[::-1]
    
    """
    plots the sectors and the arcs
    """
    patches = []
    for ang, c in zip(ang_range, colors): 
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
    
    [ax.add_patch(p) for p in patches]

    
    """
    set the labels (e.g. 'LOW','MEDIUM',...)
    """

    for mid, lab in zip(mid_points, labels): 

        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=12, \
            fontweight='bold', rotation = rot_text(mid))

    """
    set the bottom banner and the title
    """
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
    ax.add_patch(r)
    
    ax.text(0, -0.05, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=22, fontweight='bold')

    """
    plots the arrow now
    """
    
    #pos = mid_points[abs(arrow - N)]
    pos = ((arrow+2) + 1) * -90

    
    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

    """
    removes frame and ticks, and makes axis equal and tight
    """
    
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    buf = BytesIO()
    fig.savefig(buf, format='png')
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    #plt.tight_layout()
    #plt.show()
    if fname:
        fig.savefig(fname, dpi=200)
    #plt.close()
    return image_base64

# gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
#       colors='RdYlGn_r', arrow=News.objects.all().aggregate(Avg('senti_score'))['senti_score__avg'], title='News Sentiment', fname='test') 

@login_required(login_url='users/index.html')
def index(request):
	# insert sessions and insert context{} to drag out more data. GET USER COPIED ACROSS
	username = request.user
	data_input1 = News.objects.filter(newsreader=username.id).aggregate(Avg('senti_score'))['senti_score__avg']
	data_input2 = News.objects.filter(newsreader=username.id).order_by('-senti_score')[:5]
	data_input3 = News.objects.filter(newsreader=username.id).order_by('-senti_score').reverse()[:5]
	data_input4 = News.objects.filter(newsreader=username.id).aggregate(Avg('sadness'))['sadness__avg']
	data_input5 = News.objects.filter(newsreader=username.id).aggregate(Avg('joy'))['joy__avg']
	data_input6 = News.objects.filter(newsreader=username.id).aggregate(Avg('fear'))['fear__avg']
	data_input7 = News.objects.filter(newsreader=username.id).aggregate(Avg('disgust'))['disgust__avg']
	data_input8 = News.objects.filter(newsreader=username.id).aggregate(Avg('anger'))['anger__avg']
	data_input9 = News.objects.filter().aggregate(Avg('senti_score'))['senti_score__avg']
	data_input10 = Ents.objects.filter(newsreader=username.id).order_by('-entsentiscore')[:5]
	data_input11 = Ents.objects.filter(newsreader=username.id).order_by('-entsentiscore').reverse()[:5]
	if data_input4 == None:
		data_input4 = 0
	else:
		data_input4 = round(data_input4, 2)
	if data_input5 == None:
		data_input5 = 0
	else:
		data_input5 = round(data_input5, 2)
	if data_input6 == None:
		data_input6 = 0
	else:
		data_input6 = round(data_input6, 2)
	if data_input7 == None:
		data_input7 = 0
	else:
		data_input7 = round(data_input7, 2)
	if data_input8 == None:
		data_input8 = 0
	else:
		data_input8 = round(data_input8, 2)	
	if data_input1 == None:
		f = gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
	      colors='RdYlGn_r', arrow=0, title='News Sentiment', fname='test.png')
	else:
		f = gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
	      colors='RdYlGn_r', arrow=data_input1, title='News Sentiment', fname='test.png')
	if data_input9 == None:
		newsall = gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
		      colors='RdYlGn_r', arrow=0, title='News Sentiment', fname='test.png')
	else:
		newsall = gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
		      colors='RdYlGn_r', arrow=data_input9, title='News Sentiment', fname='test.png')
	return render(request, "news/index.html", {
		"news": f,
		"user": username.username,
		"top5": data_input2,
		"bottom5": data_input3,
		"sadness": data_input4,
		"joy": data_input5,
		"fear": data_input6,
		"disgust": data_input7,
		"anger": data_input8,
		"enttop5": data_input10,
		"entbot5": data_input11,
		"newsall": newsall
		})

def book(request):
	if request.method == "POST":
		username = request.user
		url_check = request.POST["Website"]
		response = natural_language_understanding.analyze(url=url_check, features=Features(categories=CategoriesOptions(limit=1),sentiment=SentimentOptions(document=True), emotion=EmotionOptions(document=True), entities=EntitiesOptions(sentiment=True,limit=3))).get_result()
		#response = natural_language_understanding.analyze(url=url_check, features=Features(categories=CategoriesOptions(limit=3),sentiment=SentimentOptions(document=True), emotion=EmotionOptions(document=True), keywords=KeywordsOptions(sentiment=True,emotion=True,limit=3),entities=EntitiesOptions(sentiment=True,limit=3))).get_result()
		dumps = json.dumps(response)
		data = json.loads(dumps)
		news_data = News(
		newsreader = username,
		newsurl = data['retrieved_url'],
		language = data['language'],
		text_characters = data['usage']['text_characters'],
		cat1 =  data['categories'][0]['label'],
		cat1_score = data['categories'][0]['score'],
		sentiment = data['sentiment']['document']['label'],
		senti_score = data['sentiment']['document']['score'],
		sadness = data['emotion']['document']['emotion']['sadness'],
		joy = data['emotion']['document']['emotion']['joy'],
		fear = data['emotion']['document']['emotion']['fear'],
		disgust = data['emotion']['document']['emotion']['disgust'],
		anger = data['emotion']['document']['emotion']['anger'])
		news_data.save()
		for x in range(3):		
			ent_data = Ents(
			newsreader = username,
			enturl = data['retrieved_url'],
			enttype = data['entities'][x]['type'],
			enttext = data['entities'][x]['text'],
			entsenti = data['entities'][x]['sentiment']['label'],
			entsentiscore = data['entities'][x]['sentiment']['score'],
			entrele = data['entities'][x]['relevance'],
			entcount = data['entities'][x]['count'],
			entcon = data['entities'][x]['confidence'])
			ent_data.save()				
		return HttpResponseRedirect(reverse("news:index1"))

	return render(request, "news/index.html", {
		"news": News.objects.filter(newsreader=request.user.id).aggregate(Avg('senti_score'))['senti_score__avg']
		})

def allusers(request):
	# insert sessions and insert context{} to drag out more data. GET USER COPIED ACROSS
	username = request.user
	data_input1 = News.objects.filter().aggregate(Avg('senti_score'))['senti_score__avg']
	data_input2 = News.objects.filter().order_by('-senti_score')[:5]
	data_input3 = News.objects.filter().order_by('-senti_score').reverse()[:5]
	data_input4 = News.objects.filter().aggregate(Avg('sadness'))['sadness__avg']
	data_input5 = News.objects.filter().aggregate(Avg('joy'))['joy__avg']
	data_input6 = News.objects.filter().aggregate(Avg('fear'))['fear__avg']
	data_input7 = News.objects.filter().aggregate(Avg('disgust'))['disgust__avg']
	data_input8 = News.objects.filter().aggregate(Avg('anger'))['anger__avg']
	data_input9 = News.objects.filter().aggregate(Avg('senti_score'))['senti_score__avg']
	data_input10 = Ents.objects.filter().order_by('-entsentiscore')[:5]
	data_input11 = Ents.objects.filter().order_by('-entsentiscore').reverse()[:5]
	if data_input4 == None:
		data_input4 = 0
	else:
		data_input4 = round(data_input4, 2)
	if data_input5 == None:
		data_input5 = 0
	else:
		data_input5 = round(data_input5, 2)
	if data_input6 == None:
		data_input6 = 0
	else:
		data_input6 = round(data_input6, 2)
	if data_input7 == None:
		data_input7 = 0
	else:
		data_input7 = round(data_input7, 2)
	if data_input8 == None:
		data_input8 = 0
	else:
		data_input8 = round(data_input8, 2)
	if data_input1 == None:
		f = gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
	      colors='RdYlGn_r', arrow=0, title='News Sentiment', fname='test.png')
	else:
		f = gauge(labels=['NEGATIVE','','','','','POSITIVE'], \
	      colors='RdYlGn_r', arrow=data_input1, title='News Sentiment', fname='test.png')
	
	return render(request, "news/allusers.html", {
		"news": f,
		"user": username.username,
		"top5": data_input2,
		"bottom5": data_input3,
		"sadness": data_input4,
		"joy": data_input5,
		"fear": data_input6,
		"disgust": data_input7,
		"anger": data_input8,
		"enttop5": data_input10,
		"entbot5": data_input11
		})
