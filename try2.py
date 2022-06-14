qn_number = 0
for lala in range(0, 2, 2):
    home_link = "https://www.indiabix.com"
    page_link = "https://www.indiabix.com/civil-engineering/"
    work_path = "C:\\Users\\Irthak Miisaaz\\OneDrive - Tribhuvan University\\Desktop\\civil sets\\With explanations - new\\"
    ## engineer
    nav_keys_civil = ["theory-of-structures", "strength-of-materials", "surveying", "building-materials", "concrete-technology", "soil-mechanics-and-foundation-engineering", "construction-management", "estimating-and-costing", "engineering-economy"]
    syllabus_civil = [3, 2, 7, 6, 5, 6, 6, 5, 4, 3, 3]
    ## sub-engineer
    nav_keys_sub = ["surveying", "building-materials", "theory-of-structures", "strength-of-materials", "hydraulics", "soil-mechanics-and-foundation-engineering", "rcc-structures-design", "building-construction", "concrete-technology", "water-supply-engineering", "waste-water-engineering", "irrigation", "highway-engineering", "estimating-and-costing", "construction-management", "airport-engineering"]
    syllabus_sub = [4, 4, 2, 2, 4, 4, 4, 2, 2, 2, 2, 4, 4, 4, 4, 2]
    nav_keys_sub, syllabus_sub = nav_keys_sub[lala:lala+2], syllabus_sub[lala:lala+2]

    for_civil = False
    create_question_bank = True
    test_phase = False
    write_to_document = False
    total_sets_needed = 200
    if test_phase: total_sets_needed = 5

    no_of_removed_qns = 0

    from bs4 import BeautifulSoup
    import bs4
    import requests
    from requests.models import HTTPError
    import urllib.request
    from io import BytesIO
    import re
    import random
    from docx import Document
    from docx.enum.style import WD_STYLE_TYPE
    from docx.shared import Pt, RGBColor, Inches
    from docx.oxml.ns import qn
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    import time, sys
    import numpy as np
    from threading_self import ThreadWithResult

    def fetch_discussions(page_link, discuss_id):
        try:
            html_text = requests.get(page_link + f'discussion-{discuss_id}').text
        except:
            return [['', '', '']]
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


    def format_qns_and_options(opts_temp):
        for index, item in enumerate(opts_temp):
            if not(type(item) is str or '<img src' in str(item)):
                try:
                    if 'class="root"' in str(item):
                        opts_temp[index] = "√" + item.text
                    else:        
                        opts_temp[index] = item.text
                except:
                    pass
        
        new_list=['']
        for i in opts_temp:
            if type(i)==str:
                new_list[len(new_list)-1]=new_list[len(new_list)-1]+i
            else:
                new_list.append('')
        out=list()
        for i in new_list:
            if i!='':
                out.append(i)
        out = ''.join(out)
        return out

    def question_fetch(page_link, nav_keys, index=0, test_phase=True):
        page_link = page_link + nav_keys[index] + '/'

        html_text = requests.get(page_link).text
        soup = BeautifulSoup(html_text, 'lxml')

        section_no = soup.select(f"a[href*={nav_keys[index]}]")[1]['href'].split('/')[-1]
        # print("Section_no: ", section_no, '\n')
        section_no_total_digits = len(section_no)
        section_no = int(section_no) - 1000
        # print("starting section_no: ", section_no)

        total_sections = sum(1 for li in soup.find('ul', class_="ul-top-left"))
        if test_phase: total_sections = 1
        # print("\ntotal_sections: ", total_sections)

        # qn = [a.text for a in soup.find_all('td', class_="bix-td-qtxt")]
        # print("\nqn:", qn)
        qens = []
        for t in range(total_sections):         # range(total_sections) to fetch from all sections 
            total_pages = str(soup.select("p[class*=mx-pager]")).count('</span>')
            if test_phase: total_pages = 10
            # print("total_pages: ", total_pages)
            for j in range(total_pages):    # range(total_pages) to fetch from all pages
                if t!=0 or j!=0:
                    curr_section = str(section_no + t*1000 + j)
                    if len(curr_section) != section_no_total_digits:
                        curr_section = '0' + curr_section
                    if len(curr_section) != section_no_total_digits:
                        curr_section = '0' + curr_section
                    if j%3 == 0:
                        print('.', end='')
                    # print(f"curr_section for t: {t} and j: {j} is ", curr_section)
                    html_text = requests.get(page_link + curr_section).text
                    soup = BeautifulSoup(html_text, 'lxml')

                qn_temp = [[format_qns_and_options(a.contents[0].contents)] for a in soup.find_all('td', class_="bix-td-qtxt")]
                
                opts_ids = [a['id'].split('_')[-1] for a in soup.find_all("table", class_= "bix-tbl-options")]
                opts = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                ans_list = [a.text for a in soup.find_all("span", class_=re.compile(r'jq-hdnakqb.*'))]

                # opts_description = []
                # threads = [ThreadWithResult(target=fetch_discussions, args=[page_link, i]) for i in opts_ids]
                # [i.start() for i in threads]
                # [i.join() for i in threads]

                # discussions_in_page = [i.result for i in threads]

                discussions_in_page = []
                for ax in opts_ids:
                    discussions_in_page.append(fetch_discussions(page_link, ax))
                
                for k in range(len(qn_temp)):
                    qn_temp[k].append(discussions_in_page[k])
                qens.append(qn_temp)
        qn_subwise = []
        for i in qens:
            for j in i:
                qn_subwise.append(j)
        # print(len(qn_subwise[1]))
        filtered = qn_subwise
        return filtered

    if for_civil:
        nav_keys = nav_keys_civil
        syllabus = syllabus_civil
    else:
        nav_keys = nav_keys_sub
        syllabus = syllabus_sub


    print('fetching data ', end='')
    threads = [ThreadWithResult(target=question_fetch, args=[page_link, nav_keys, i, test_phase]) for i in range(len(nav_keys))]
    for i in threads:
        i.start()
    [i.join() for i in threads]

    grand_collection = [i.result for i in threads]

    all_quens = []
    for i in grand_collection:
        for x in i:
            all_quens.append(x)

    # print(all_quens[1])
    with open(f"quens_coll{lala}.txt", "w", encoding="utf-8") as file:
        for y, x in enumerate(all_quens):
            file.write(rf'{qn_number + y + 1}. {x[0]}')
            file.write('\n')
            for i in x[1]:
                file.write('\t')
                for j in i[:2]:
                    file.write(rf'{j}')
                    file.write(', ')
                temp = ' $% '.join(i[2].split('\n'))
                file.write(rf'{temp}')
                file.write('\n')
            file.write('\n\n\n')

    qn_number += len(all_quens)
    print('\n')
    time.sleep(5)