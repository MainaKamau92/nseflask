import urllib.error as error

from flask import Flask
from flask_cors import CORS, cross_origin

from crawler import extract_html, get_data_by_date

app = Flask(__name__)
CORS(app, support_credentials=True)


def validate_change(stock):
    try:
        return stock['d']
    except KeyError:
        return None


def validate_percentage_change(stock):
    try:
        return stock['e']
    except KeyError:
        return None


def validate_gain_or_loss(stock):
    try:
        return stock['f']
    except KeyError:
        return None


def business_daily_ticker():
    URL = 'https://tickers.mystocks.co.ke/ticker/TAPE$?type=bda;f=mslFrame0;d=www.businessdailyafrica.com'
    soup = extract_html(URL)
    stocks = soup.findAll("i")
    data = []
    for stock in stocks:
        data.append(dict(code=stock['a'], latest=stock['b'],
                         change=validate_change(stock),
                         percent_change=validate_percentage_change(stock),
                         gain_or_loss=validate_gain_or_loss(stock)))
    return data


def back_up_live_market():
    URL = 'https://tickers.mystocks.co.ke/ticker/RMWX$?app=FIB;f=mslFrame0;d=fib.co.ke'
    soup = extract_html(URL)
    stocks = soup.findAll("i")
    data = []
    for stock in stocks:
        data.append(dict(code=stock['a'], percentage_change=stock['e'],
                         latest=stock['c'], change=stock['d']))
    return data


@app.route('/live-market')
@cross_origin(supports_credentials=True)
def live_stocks():
    try:
        data = business_daily_ticker()
        return dict(live_data=data)
    except error.HTTPError:
        data = back_up_live_market()
        return dict(live_data=data)
    except:
        data = back_up_live_market()
        return dict(live_data=data)


@app.route('/stocks/<stock_date>')
def stocks_prices_per_date(stock_date):
    response_obj = get_data_by_date(date_=stock_date)
    return response_obj


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
        ENV='development'
    )
    app.run(debug=True, port=5000)
