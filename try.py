from bs4 import BeautifulSoup, element
import bs4
import requests
import re
from code import *

home_link = "https://www.indiabix.com"
img_link = "/_files/images/civil-engineering/strength-of-materials/140-6.218-3.png"

page_link = "https://www.indiabix.com/civil-engineering/surveying/discussion-637"


# a = soup.select('div[class*=bix-ans-description]')
# print(a[0].a['href'])

# opts_temp = [a.text if a.text else home_link + a.img['src'] for a in soup.find_all('td', id=re.compile(rf'tdOptionDt...{2448}'))]
# print(home_link in opts_temp[0])
# print(b)

# qn_temp = [[[a.text, home_link + a.img['src']]] if a.img else [a.text] for a in soup.find_all('td', class_="bix-td-qtxt")]
# print(qn_temp[:2])


# qns = [i for i in soup.find_all('td', id=re.compile(rf'tdOptionDt...{4718}'))]
# a = str(qns[1]).split(str(qns[1].img))
# b = a[0].split('<p>')[-1]
# index = len(b)

# txt = qns[1].text
# print(txt[:index-1], txt[index:])
# print(txt)


# index = 3
# opts_temp = qns[index].contents
# opts_temp.append([1, 2])
# opts_temp = opts_temp + ['gane', 'sh', 'is', '', '', ['good'], '']
# for index, item in enumerate(opts_temp):
#     if not(type(item) is str or '<img src' in str(item)):
#         try:
#             if 'class="root"' in str(item):
#                 opts_temp[index] = "√" + item.text
#             else:        
#                 opts_temp[index] = item.text
#         except:
#             pass
# new_list=['']
# for i in opts_temp:
#     if type(i)==str:
# 	    new_list[len(new_list)-1]=new_list[len(new_list)-1]+i
#     else:
#         new_list.append(i)
#         new_list.append('')
# out=list()
# for i in new_list:
#     if i!='':
#         out.append(i)
# print(out)
# print(opts_temp)

# my_list = [i['src'] if type(i)==bs4.element.Tag else i for i in qns[0].contents[0].contents]
# print(my_list)

# from docx import Document
# from docx.shared import Inches
# from io import BytesIO
# import urllib.request

# def gen_image(url_value):
#         image_from_url = urllib.request.urlopen(url_value)
#         io_url = BytesIO()
#         io_url.write(image_from_url.read())
#         io_url.seek(0, 0)
#         return io_url

# with open('try.docx', 'w') as a:
#     pass

# document = Document()
# p = document.add_paragraph('Picture bullet section')
# r = p.add_run()
# r.add_picture(gen_image(home_link+img_link), height=Inches(0.3))
# p = p.insert_paragraph_before('My picture title', 'Heading 1')
# document.save('try.docx')


discuss_id = 637
def fetch_discussions(discuss_id):
    html_text = requests.get(page_link + f'discussion-{discuss_id}').text
    soup_discuss = BeautifulSoup(html_text, 'lxml')

    discussion_html = soup_discuss.find_all('div', class_='bix-sun-discussion')
    discussion_list = []

    for discussion in discussion_html:
        user_detail = discussion.select('td[class="user-details"]')[0].find_all('span')
        user = user_detail[0].text
        date = user_detail[1].text.split(',')[-1].strip()[:-1]
        discuss_content = discussion.select('td[class="user-content"]')[0].text
        discussion_list.append([user, date, discuss_content])
    
    return discussion_list
