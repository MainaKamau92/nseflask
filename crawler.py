import urllib.request as rq
from datetime import date

from bs4 import BeautifulSoup


def extract_html(url):
    html = rq.urlopen(url).read()
    return BeautifulSoup(html, "lxml")


def extract_url_data(soup):
    table = soup.find("table", {"class": "tblHoverHi"})
    data = []
    for row in table.findAll("tr"):
        shareDetails = list()
        shareElements = list()
        for element in row.findAll("td"):
            # the share categories i.e banking, manufacturing
            for heading in element.findAll("h3"):
                _heading = heading.string
            # the share company name
            for item in element.findAll("a"):
                shareElements.append(item.string)
            # the shares details i.e price,volume
            if element.string != heading.string:
                shareElements.append(element.string)
        # removes empty and None arrays, clean up from html extracted data
        if shareElements != [] and len(shareElements) > 1:
            # code
            shareDetails.append(shareElements[0])
            # name
            shareDetails.append(shareElements[1])
            # lowest price
            if shareElements[5] is None or shareElements[5] == '-':
                shareDetails.append(shareElements[5])
            else:
                shareDetails.append(float(shareElements[5].replace(',', '')))
            # highest price
            if shareElements[6] is None or shareElements[6] == '-':
                shareDetails.append(shareElements[6])
            else:
                shareDetails.append(float(shareElements[6].replace(',', '')))
            # price
            if shareElements[7] is None or shareElements[7] == '-':
                shareDetails.append(shareElements[7])
            else:
                shareDetails.append(float(shareElements[7].replace(',', '')))
            # previous day's price
            if shareElements[8] is None or shareElements[8] == '-':
                shareDetails.append(shareElements[8])
            else:
                shareDetails.append(float(shareElements[8].replace(',', '')))
            # volume
            if (shareElements[12] is None) or (shareElements[12] == '-'):
                shareDetails.append(shareElements[12])
            else:
                shareDetails.append(str(shareElements[12].replace(',', '')))
            data.append(shareDetails)
    return data


def get_data_by_date(date_):
    url = "https://live.mystocks.co.ke/price_list/" + date_
    soup = extract_html(url)
    if len(extract_url_data(soup)) > 0:
        year, month, day = int(date_[0:4]), int(date_[4:6]), int(date_[6:8])

        data = [dict(code=i[0], name=i[1],
                     lowest_price_of_day=i[2], highest_price_of_the_day=i[3],
                     closing_price=i[4], previous_day_closing_price=i[5],
                     volume_traded=i[6]) for i in extract_url_data(soup)]
        stock_date = date(year=year, month=month, day=day)
        response_object = {
            "date": stock_date,
            "data": data
        }
        return response_object
    return extract_url_data(soup)
