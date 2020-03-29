from flask import render_template, request, make_response
from app.misc import misc
from app.misc.forms import DisplayInfoForm
import urllib
from urllib.error import HTTPError
import json
import datetime
import feedparser

RSS_FEEDS = {'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'vnexpress': 'https://vnexpress.net/rss/tin-moi-nhat.rss',
             'dantri': 'https://dantri.com.vn/trangchu.rss'}

DEFAULTS = {'publication': 'cnn',
            'city': 'London, UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

# An example how to use default value in route decoration
# @misc.route('/misc/weather', methods=['GET', 'POST'], defaults={'city_name' : DEFAULTS['city']})
@misc.route('/misc/info', methods=['GET', 'POST'])
def diplayInfo():

    # Get the parsed data from json obj
    rate_data = get_rates()
    currencies = rate_data.keys()

    form = DisplayInfoForm()
    # Create dynamic select field in wtforms
    # Remember [choices=] requires tuples to work
    form.currency_from.choices = [(currency, currency)
                                  for currency in currencies]
    form.currency_to.choices = [(currency, currency)
                                for currency in currencies]

    if form.validate_on_submit():
        city_name = form.city.data
        publication = form.publication.data
        currency_from = form.currency_from.data
        currency_to = form.currency_to.data
    else:
        city_name = request.args.get('city')
        publication = request.args.get('publication')
        currency_from = get_value_fallback_cookie('currency_from')
        currency_to = get_value_fallback_cookie('currency_to')

    city_name, weather = get_weather(city_name)

    max_headlines = 10 
    publication, articles = get_publication(publication)

    rate = round(rate_data.get(currency_to)/rate_data.get(currency_from))

    response = make_response(render_template('info.html',
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             publication=publication,
                                             articles=articles,
                                             max=max_headlines,
                                             form=form,
                                             city=city_name,
                                             weather=weather))

    # Saving cookies
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city_name, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


def get_publication(publication):
    if not publication or publication.lower() not in RSS_FEEDS:
        publication = get_value_fallback_cookie('publication')
    else:
        publication = publication.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return publication, feed['entries']


def get_weather(city_name):

    # Empty city name? Fall back to cookie or default value
    if not city_name:
        city_name = get_value_fallback_cookie('city')

    city = urllib.parse.quote(city_name)
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=785f6ef1ac26c66cfe8dd3d110e0bb3c".format(
        city)

    # Retrieve the data
    # Catch 404 error here
    try:
        data = urllib.request.urlopen(url).read()
        parsed_data = json.loads(data)
        if parsed_data.get("weather"):
            weather = {"description": parsed_data["weather"][0]["description"],
                       "temperature": parsed_data["main"]["temp"],
                       "city": parsed_data["name"],
                       "country": parsed_data["sys"]["country"]}
    except urllib.error.HTTPError:
        weather = None
    return city_name, weather


def get_rates():
    url = "https://openexchangerates.org//api/latest.json?app_id=4e1b04781d834b7eb4aa731ecc0e79a9"
    data = urllib.request.urlopen(url).read()
    return json.loads(data).get('rates')


def get_value_fallback_cookie(key):
    # Get default value from cookies or DEFAULTS dictionary
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]
