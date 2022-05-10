from bottle import route, run, template
from db import News, session
from bottle import redirect, request
from scraputils import get_news
from bayes import NaiveBayesClassifier


@route('/')
@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label/')
def add_label():
    s = session()
    lb = request.query.label
    cur_id = request.query.id
    post = s.query(News).filter(News.id == cur_id).all()[0]
    post.label = lb
    s.commit()
    redirect('/news')


@route('/update_news')
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 3)
    for new in news:
        if len(s.query(News).filter(News.author == new['author'] and News.title == new['title']).all()) == 0:
            elem = News(
            title = new['title'],
            author=new['author'],
            url = new['url'],
            comments = new['comments'],
            points = new['points'],
            )
            s.add(elem)
    s.commit()
    redirect('/news')

@route('/recommendations')
def recommendations():
    s = session()
    empty = s.query(News).filter(News.label == None).all()
    simp_rows = [x.title for x in empty ]
    class_rows = [x.title for x in s.query(News).filter(News.label != None).all() ]
    labels = [news.label for news in s.query(News).filter(News.label != None).all()]
    model = NaiveBayesClassifier()
    model.fit(class_rows, labels)
    predicts = model.predict(simp_rows)
    for x in range(len(predicts)):
        empty[x].label = predicts[x]
    classified_news = [x  for x in empty if x.label == 'good']
    classified_news.extend( [x  for x in empty if x.label == 'maybe'] )
    classified_news.extend( [x  for x in empty if x.label == 'never'] )
    return template('recs.tpl', rows=classified_news[1:])


if __name__ == "__main__":
    run(host="localhost", port=8080)

