import feedparser
from flask import Flask,render_template,request
app = Flask(__name__)
BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640'}
# @app.route('/')
# def home():
#     feed = feedparser.parse(BBC_FEED)
#     # first_article = feed['entries'][0]
#     # return '''<html>
#     #           <body>
#     #           <h1> BBC Headlines </h1>
#     #           <b>{0}</b> <br/>
#     #           <i>{1}</i> <br/>
#     #           <p>{2}</p> <br/>
#     #           </body>
#     #           </html>'''.format(first_article.get('title'), first_article.get('published'), first_article.get('summary'))
#     # return render_template('home.html',title = first_article.get('title'), published = first_article.get('published'), summary = first_article.get('summary'))
#     return render_template('home.html', articles = feed['entries'])
# @app.route('/<publicationname>')
# def get_news(publicationname):
#     feed = feedparser.parse(RSS_FEEDS[publicationname])
#     # first_article = feed['entries'][0]
#     # return '''<html>
#     #           <body>
#     #           <h1> BBC Headlines </h1>
#     #           <b>{0}</b> <br/>
#     #           <i>{1}</i> <br/>
#     #           <p>{2}</p> <br/>
#     #           </body>
#     #           </html>'''.format(first_article.get('title'), first_article.get('published'), first_article.get('summary'))
#     # return render_template('home.html',title = first_article.get('title'), published = first_article.get('published'), summary = first_article.get('summary'))
#     return render_template('home.html', articles = feed['entries'])
@app.route('/',methods = ['GET', 'POST'])
def get_news():
    publicationname = request.form['name']
    if not publicationname or publicationname.lower() not in RSS_FEEDS:
        publicationname = 'bbc'
    else:
        publicationname = request.form['name']
    feeds = feedparser.parse(RSS_FEEDS[publicationname])
    return render_template('home.html', articles = feeds['entries'])
if __name__ == '__main__':
    app.run(port=int("3000"),debug = True)