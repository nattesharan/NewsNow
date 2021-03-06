import feedparser
from flask import Flask,render_template,request,make_response
import datetime
import urllib
import urllib2
import json
app = Flask(__name__)
BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://indiatoday.intoday.in/rss/homepage-topstories.jsp'}
@app.route('/',methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        publicationname = request.form['name'].lower()
        for i in RSS_FEEDS:
            if i == publicationname:
                errors = False
                break
            else:
                errors = True
                publicationname = 'bbc'
        if not errors:
            articles = get_news(publicationname)
    else:
        publicationname = request.cookies.get('publicationname')
        if publicationname == None:
            publicationname = 'bbc'
        else:
            publicationname = request.cookies.get('publicationname')
        feeds =  feedparser.parse(RSS_FEEDS[publicationname])
        articles = feeds['entries']
    resp = make_response(render_template('home.html',articles = articles))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    resp.set_cookie('publicationname',publicationname, expires = expires)
    return resp
def get_news(publicationname):
    feeds = feedparser.parse(RSS_FEEDS[publicationname])
    return feeds['entries']
@app.route('/temp',methods = ['POST','GET'])
def temp():
    if request.method == 'POST':
        city = request.form['city']
        if city == '':
            city = 'Hyderabad'
        else:
            city = request.form['city']
        weather = get_weather(city)
    else:
        api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=678c9a313a7a3293f3186ba63375e0c6'
        city = request.cookies.get('city')
        if city == None:
            city = 'Hyderabad'
        else:
            city = request.cookies.get('city')
        query = urllib.quote(city)
        url = api_url.format(query)
        data = urllib2.urlopen(url).read()
        parsed = json.loads(data)
        weather = get_weather(city)
    resp = make_response(render_template('temp.html',weather = weather))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    resp.set_cookie('city',city,expires=expires)
    return resp
def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=678c9a313a7a3293f3186ba63375e0c6'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            'description':parsed['weather'][0]['description'],
            'temperature':parsed['main']['temp'],
            'city':parsed['name'],
            'country': parsed['sys']['country']
        }
    return weather
if __name__ == '__main__':
    app.run(port=int("3000"),debug = True)