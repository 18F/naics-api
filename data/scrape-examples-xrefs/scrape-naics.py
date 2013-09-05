#!/usr/bin/env python

from re import compile
from csv import DictReader
from urllib import urlopen, urlencode
from bs4 import BeautifulSoup

def find_examples(soup):
    ''' Generate a list of examples from a starting point.
    '''
    el = soup.find(text='Illustrative Examples:')
    
    if not el:
        # Nothing.
        return
    
    for i in range(2):
        el = el.nextSibling
        
        if el.name != 'br':
            # There are supposed to be two breaks after "Illustrative Examples"
            return
    
    while True:
        el = el.nextSibling
    
        if el.name is not None:
            # Expected plain text here.
            return
        
        yield unicode(el)

        el = el.nextSibling
    
        if el.name != 'br':
            # Expected a break here
            return

def find_crossreferences(soup):
    '''
    '''
    el = soup.find(text=compile(r'^Cross-References.'))
    
    if not el:
        # Nothing.
        return
    
    el = el.nextSibling.nextSibling.nextSibling
    
    if el.name != 'ul':
        # Expected an unordered list after some blank lines.
        return
    
    for el in el.find_all('li'):
        code, text = None, ''
    
        for el in el.contents:
            if el.name == 'a':
                text += el.string
                code = el.string
            else:
                text += unicode(el)
        
        yield code, text

rows = DictReader(urlopen('http://forever.codeforamerica.org.s3.amazonaws.com/NAICS/6-digit_2012_Codes.csv'))

rows = [
    {'2012 NAICS Code': 423390, '2012 NAICS Title': 'Other Construction Material Merchant Wholesalers'},
    {'2012 NAICS Code': 111110, '2012 NAICS Title': 'Soybean Farming'},
    {'2012 NAICS Code': 111310, '2012 NAICS Title': 'Orange Groves'},
    ]

for row in rows:

    q = dict(code=row['2012 NAICS Code'], search='2012 NAICS Search')
    url = 'http://www.census.gov/cgi-bin/sssd/naics/naicsrch?' + urlencode(q)
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    soup = soup.find(id='middle-column').find(class_='inside')
    
    print row['2012 NAICS Title']
    
    for example in find_examples(soup):
        print ' ', example
    
    for (code, text) in find_crossreferences(soup):
        print ' ', code, text
