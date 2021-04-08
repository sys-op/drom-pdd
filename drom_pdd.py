#import http
import urllib.request
from bs4 import BeautifulSoup
import os
from PIL import Image

base_url = 'https://drom.ru/pdd/bilet'

width = 604
height = 225
image = Image.new('RGB', (width, height))

tickets = range(1,41)
for ticket in tickets:
    url = f'{base_url}_{ticket}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        page = resp.read()
    html = BeautifulSoup(page, features='lxml', multi_valued_attributes=None)

    count = 0
    dir = f'ticket_{ticket}'

    if not os.path.exists(dir):
        os.mkdir(dir)

    for div in html.findAll('div'):
        if div.get('class') == 'pdd-ticket b-media-cont':
            for div_img in div.findAll('div'):
                if div_img.get('class') == 'b-media-cont':
                    count += 1
                    fname = os.path.join(dir,f'{ticket}_{count}.jpg')
                    print(f'Ticket №{ticket}, Answer №{count}')
                    img = div_img.contents[1]
                    src = img.get('src')
                    if src is None:
                        image.save(fname)
                    else:
                        urllib.request.urlretrieve(src,fname)
