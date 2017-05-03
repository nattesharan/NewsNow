import feedparser
from flask import Flask,render_template,request
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
        return render_template('home.html',articles = articles)
    else:
        feeds =  feedparser.parse(RSS_FEEDS['bbc'])
        articles = feeds['entries']
        return render_template('home.html',articles = articles)
def get_news(publicationname):
    feeds = feedparser.parse(RSS_FEEDS[publicationname])
    return feeds['entries']
if __name__ == '__main__':
    app.run(port=int("3000"),debug = True)