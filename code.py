home_link = "https://www.indiabix.com"
page_link = "https://www.indiabix.com/civil-engineering/"
work_path = "C:\\Users\\Irthak Miisaaz\\OneDrive - Tribhuvan University\\Desktop\\civil sets\\With explanations - new\\"
## engineer
nav_keys_civil = ["theory-of-structures", "strength-of-materials", "surveying", "building-materials", "concrete-technology", "soil-mechanics-and-foundation-engineering", "construction-management", "estimating-and-costing", "engineering-economy"]
syllabus_civil = [3, 2, 7, 6, 5, 6, 6, 5, 4, 3, 3]
## sub-engineer
nav_keys_sub = ["surveying", "building-materials", "theory-of-structures", "strength-of-materials", "hydraulics", "soil-mechanics-and-foundation-engineering", "rcc-structures-design", "building-construction", "concrete-technology", "water-supply-engineering", "waste-water-engineering", "irrigation", "highway-engineering", "estimating-and-costing", "construction-management", "airport-engineering"]
syllabus_sub = [4, 4, 2, 2, 4, 4, 4, 2, 2, 2, 2, 4, 4, 4, 4, 2]

for_civil = False
create_question_bank = True
test_phase = False
write_to_document = True
total_sets_needed = 200
if test_phase: total_sets_needed = 5

no_of_removed_qns = 0
removed_qn_index = [0]
removed_qn_list = []

from os import remove
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
            new_list.append(i)
            new_list.append('')
    out=list()
    for i in new_list:
        if i!='':
            out.append(i)
    return out

def filter_questions(qn_subwise, index):
    global no_of_removed_qns
    global removed_qn_index
    global removed_qn_list
    ########### filters here! #############
    # filter out questions containing empty options
    temp_qn_subwise = qn_subwise
    unremoved_list = qn_subwise.copy()
    length_of_unremoved_list = len(qn_subwise)
    removed_qn_index.append(length_of_unremoved_list)
    # print(temp_qn_subwise[2][1])
    for j in temp_qn_subwise:
        try:
            if '' in j[1]:
                # print(qn_subwise[i])
                # print('\n')
                removed_qn_list.append([sum(removed_qn_index[:index+1]) + unremoved_list.index(j) + 1, j[0]])
                qn_subwise.remove(j)
                no_of_removed_qns += 1
                # if nav_keys[index] == 'strength-of-materials':
                #     print(j)
        except:
            # print('qn removed')
            removed_qn_list.append([sum(removed_qn_index[:index+1]) + unremoved_list.index(j) + 1, j[0]])
            qn_subwise.remove(j)
            no_of_removed_qns += 1
    # change 5-option questions to 4-option questions
    temp_qn_subwise = qn_subwise
    for j in temp_qn_subwise:
        if len(j[1]) == 6:
            ans_option = j[1][-1]
            if ans_option == 0:
                j[1].pop(-2)
            else:
                j[1].pop(0)
                j[1][-1] = j[1][-1] - 1
        if len(j[1]) >= 7:
            removed_qn_list.append([sum(removed_qn_index[:index+1]) + unremoved_list.index(j) + 1, j[0]])
            qn_subwise.remove(j)
            no_of_removed_qns += 1

    # Again filter out questions containing empty options
    for j in qn_subwise:
        if '' in j[1]:
            # print(qn_subwise[i])
            # print('\n')
            removed_qn_list.append([sum(removed_qn_index[:index+1]) + unremoved_list.index(j) + 1, j[0]])
            qn_subwise.remove(j)
            no_of_removed_qns += 1
            # if nav_keys[index] == 'strength-of-materials':
            #     print(j)

    # filter out questions containing figures or indian datas.    
    for j in qn_subwise:
        if 'India' in j[0] or 'india' in j[0]:
            removed_qn_list.append([sum(removed_qn_index[:index+1]) + unremoved_list.index(j) + 1, j[0]])
            qn_subwise.remove(j)
            no_of_removed_qns += 1

    # filter out questions with options that are incomplete(end with '=') due to presence of math formulas.
    for j in qn_subwise:
        for k in j[1]:
            if k and type(k) == str and k[-1] == '=':
                # print(j)
                removed_qn_list.append([sum(removed_qn_index[:index+1]) + unremoved_list.index(j) + 1, j[0]])
                qn_subwise.remove(j)
                no_of_removed_qns += 1
                break
    ############# end of filters! #############
    return qn_subwise

# fetch questions from india-bix
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
                
            for k, l in enumerate(opts_ids):
                opts_temp = [format_qns_and_options(a.contents) for a in soup.find_all('td', id=re.compile(rf'tdOptionDt...{l}'))]
                opts_temp.append(opts.index(ans_list[k]))

                qn_temp[k].append(opts_temp)
            qens.append(qn_temp)
    qn_subwise = []
    for i in qens:
        for j in i:
            qn_subwise.append(j)
    # print(len(qn_subwise[1]))
    filtered = filter_questions(qn_subwise, index)
    return filtered
    
# fetch questions from text file for drawing and professional practice
def fetch_from_file(qn_file, ans_file):
    file_options = ['a', 'b', 'c', 'd', 'e', 'f']
    with open(qn_file, 'r', encoding='utf-8') as file_a:
        file_qn_content = file_a.read()
    
    with open(ans_file, 'r', encoding='utf-8') as file_ans:
        file_ans_content = file_ans.read()

    file_qns = [i.split('\n', 1) for i in file_qn_content.split('\n\n')]
    file_qns.pop(-1)

    file_ans = file_ans_content.split('\n')
    file_ans.pop(-1)

    ## debugging
        # print('question list length', len(file_qns))
        # print('answer list length', len(file_ans))
        # print('\n')
        # print(file_qns[-5:])
        # print('\n')
        # print(file_ans[-5:])
    if not len(file_qns) == len(file_ans):
        print('ERROR!!! Question and Answer list don\'t match for selected files.-=')
        sys.exit()

    for x, i in enumerate(file_qns):
        a = i[1]
        i[1] = [j.split(' ', 1).pop(1) for j in a.split('\n')]
        for index, item in enumerate(i[1]):
            if item == '' or item == ' ':
                i[1].pop(index)
        i[1] = [k.strip() for k in i[1]]
        if len(i[1]) < 4: print(f"Check for qn {x+1}")
        i[0] = ''.join(i[0].split(' ', 1).pop(1)).strip()
        i[1].append(file_options.index(file_ans[x]))

    # print(file_qns[-10:-1])
    return file_qns

## write to document
def document_write(qn_all, bank_no, description_list=None):
    document = Document()
    sections = document.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    section = document.sections[0]

    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')[0]
    cols.set(qn('w:num'), '1')

    def gen_image(url_value):
        try:
            image_from_url = urllib.request.urlopen(url_value)
        except:
            print('\n', url_value, 'is giving error!')
            return r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\With explanations - new\a.png"
        io_url = BytesIO()
        io_url.write(image_from_url.read())
        io_url.seek(0, 0)
        return io_url
    
    def generate_url_from_img(a):
        return home_link + a['src']

    def writedocx(content, font_name = 'Times New Roman', font_size = 11, font_bold = False, font_italic = False, font_underline = False, color = RGBColor(0, 0, 0),
                before_spacing = 0, after_spacing = 8, line_spacing = 1.08, keep_together = False, keep_with_next = False, page_break_before = False,
                widow_control = True, align = 'left', style = '', run=False):
        paragraph = document.add_paragraph(str(content))
        paragraph.style = document.styles.add_style(style, WD_STYLE_TYPE.PARAGRAPH)
        font = paragraph.style.font
        font.name = font_name
        font.size = Pt(font_size)
        font.bold = font_bold
        font.italic = font_italic
        font.underline = font_underline
        font.color.rgb = color
        paragraph_format = paragraph.paragraph_format
        paragraph_format.space_before = Pt(before_spacing)
        paragraph_format.space_after = Pt(after_spacing)
        paragraph.line_spacing = line_spacing
        paragraph_format.keep_together = keep_together
        paragraph_format.keep_with_next = keep_with_next
        paragraph_format.page_break_before = page_break_before
        paragraph_format.widow_control = widow_control
        if align.lower() == 'left':
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        elif align.lower() == 'center':
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        elif align.lower() == 'right':
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        elif align.lower() == 'justify':
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        else:
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        if run:
            r = paragraph.add_run()
            return r
    
    if for_civil:
        writedocx(f'***Engineer***', style = 'axerxodfajfl', align='center')
    else:
        writedocx(f'***Sub Engineer***', style = 'axerxodfajfl', align='center')
    qn_all = qn_all
    total_questions = len(qn_all)
    option_numbers = ['a', 'b', 'c', 'd', 'e']

    st_num = 97
    st = chr(st_num)
    for i in range(total_questions):
        question = qn_all[i][0]
        options = qn_all[i][1]
        answer = int(options[-1])
        options = options[:-1]
        total_options = len(options)
        height = Inches(0.4)
        r = None
        for index, item in enumerate(question):
            if len(question) > 1:
                if type(item) == str and not r:
                    r = writedocx(f'{i+1}. {item}', style = st, run=True)
                elif type(item) == bs4.element.Tag and not r:
                    r = writedocx(f'{i+1}. ', style = st, run=True)
                    r.add_picture(gen_image(generate_url_from_img(item)), height=height)
                elif type(item) == bs4.element.Tag and r and question[-1]==item:
                    document.add_picture(gen_image(generate_url_from_img(item)))
                elif type(item) == bs4.element.Tag and r:
                    r.add_picture(gen_image(generate_url_from_img(item)), height=height)
                elif type(item) == str and r:
                    r.add_text(item)
                else:
                    pass
            else:
                writedocx(f'{i+1}. {item}', style = st)
            # print(question["image"], '\n')
            st += chr(random.randint(97, 122))
        r = None

        for j in range(total_options):
            # is_opt_only_image = False
            # is_opt_both_image_and_text = False
            # is_opt_only_text = False

            curr_option = options[j]
            # if type(curr_option) == dict:
            #     if len(curr_option) == 1:
            #         is_opt_only_image = True
            #     else:
            #         is_opt_both_image_and_text = True
            # else:
            #     is_opt_only_text = True
            # # print(j, ', ', answer, '\n')

            font_bold = False
            if j == answer:
                font_bold = True
                correct_option = option_numbers[j].upper()
                st += 'a'
            else:
                st += 'b'

            for x in curr_option:
                if len(curr_option) > 1:
                    if type(x) == str and not r:
                        r = writedocx(f'    {option_numbers[j]}. {x}', font_bold=font_bold, style=st, run=True)
                    elif type(x) == bs4.element.Tag and not r:
                        r = writedocx(f'    {option_numbers[j]}. ', font_bold=font_bold, style=st, run=True)
                        r.add_picture(gen_image(generate_url_from_img(x)), height=height)
                    elif type(x) == bs4.element.Tag and r:
                        r.add_picture(gen_image(generate_url_from_img(x)), height=height)
                    elif type(x) == str and r:
                        r.add_text(x)
                    else:
                        print("Couldn't write {options}!\n")
                else:
                    if type(x) == str:
                        writedocx(f'    {option_numbers[j]}. {x}', font_bold=font_bold, style=st)
                    elif type(x) == bs4.element.Tag:
                        r = writedocx(f'    {option_numbers[j]}. ', font_bold=font_bold, style=st, run=True)
                        r.add_picture(gen_image(generate_url_from_img(x)), height=height)
                    else:
                        print(f"Couldn't write {options}!\n")
                st += 'x'
            r = None
            # print(question["image"], '\n')
            # if is_opt_only_image:
            #     r = writedocx(f'    {option_numbers[j]}. ', font_bold=font_bold, style=st, run=True)
            #     r.add_picture(gen_image(curr_option["image"]), height=height)
            #     # print(curr_option["image"], '\n')
            # elif is_opt_only_text:
            #     writedocx(f'    {option_numbers[j]}. {options[j]}', font_bold=font_bold, style=st)
            # else:
            #     r = writedocx(f'    {option_numbers[j]}. {curr_option["text"]}', font_bold=font_bold, style=st, run=True)
            #     r.add_picture(gen_image(curr_option["image"]), height=Inches(0.3))
            #     # print(curr_option['image'], '\n')
        st += chr(random.randint(97, 122))
        writedocx(f"Explanation: Option {correct_option} is correct.", style=st)
        st += chr(random.randint(97, 122))
        desc_content = '\n'.join(description_list[i].split(' $% '))
        writedocx(f"{desc_content}\n", style=st)
        st += chr(random.randint(97, 122))

        if i%20 == 0:
            st_num += 1
            st = chr(st_num)
            # pass
            print('.', end='')
    
    core_properties = document.core_properties
    core_properties.author  = 'Ganesh Dhungana'
    core_properties.comments = ''
    if test_phase:
        document.save(work_path + rf'tests\test_file{bank_no + 1}.docx')
    else:
        if not create_question_bank:
            if not for_civil:
                document.save(work_path + rf'sets_subengineer\set_sub{bank_no + 200 - total_sets_needed + 1}.docx')    #Uncomment this for creating sets
            else:
                document.save(work_path + rf'sets_engineer\set_{bank_no + 1}.docx')    #Uncomment this for creating sets
        else:
            if not for_civil:
                document.save(work_path + rf'banks_sub1\bank_qn[{1+sum(syllabus_sub[:bank_no])}-{sum(syllabus_sub[:bank_no+1])}].docx')    #Uncomment this for creating banks
            else:
                document.save(work_path + rf'banks\bank_qn[{1+sum(syllabus_civil[:bank_no])}-{sum(syllabus_civil[:bank_no+1])}].docx')    #Uncomment this for creating banks

## main execution
def main(home_link, page_link, work_path, nav_keys_civil, syllabus_civil, nav_keys_sub, syllabus_sub):
    if for_civil:
        nav_keys = nav_keys_civil
        syllabus = syllabus_civil
    else:
        nav_keys = nav_keys_sub
        syllabus = syllabus_sub

    print('fetching data ', end='')
    threads = [ThreadWithResult(target=question_fetch, args=[page_link, nav_keys, i, test_phase]) for i in range(len(nav_keys))]
    [i.start() for i in threads]
    [i.join() for i in threads]

    grand_collection = [i.result for i in threads]

    if for_civil:
        drawing_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\drawing.txt"
        drawing_answer_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\drawing_answer.txt"
        drawing_questions = fetch_from_file(drawing_file, drawing_answer_file)

        print('\n\n')
        pp_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\pp.txt"
        pp_answer_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\pp_answer.txt"
        pp_questions = fetch_from_file(pp_file, pp_answer_file)

        grand_collection.insert(8, drawing_questions)
        grand_collection.append(pp_questions)

    if create_question_bank:    #create question bank
        qn_all = grand_collection 
    else:    #create sets
        sets_collection = []
        for k in range(total_sets_needed): 
            set_qns = []
            for i, j in enumerate(grand_collection):
                rand_qn_nos = random.sample(range(len(j)), syllabus[i])
                # print(f'\n{i}. ', rand_qn_nos)
                # print('\n', j)
                rand_qns = [j[k] for k in rand_qn_nos]
                set_qns += rand_qns
            sets_collection.append(set_qns)

        qn_all = sets_collection   

    ################### print to console ########################
    print('\nFinished fetching data!\n')
    print(f"{no_of_removed_qns} questions are removed!\n")
    for a, b in removed_qn_list:
        print(f'{a}. {b}\n')

    total_questions = 0
    for qnx in qn_all:
        for qnxi in qnx:
            total_questions += 1
    
    print(f"Total number of questions: {total_questions}\n")

    # print(len(qn_all))
    # for i, j in enumerate(qn_all[3]):
    #     print(f'{i+1}. {j}\n')

    with open('optimized.txt', 'r', encoding='utf-8') as file:
        description_list_all = file.read().split('\n')

    sets_length = [len(i) for i in qn_all]
    description_list = [0 for i in sets_length]
    for index in range(len(sets_length)):
        description_list[index] = description_list_all[sum(sets_length[:index]):sum(sets_length[:index+1])]
    
    if write_to_document:
        print('Writing to document ', end='')
        if create_question_bank:
            added_banks = 0
            if for_civil:
                added_banks = 2
            threads = [ThreadWithResult(target=document_write, args=[qn_all[i], i, description_list[i]]) for i in range(len(nav_keys)+added_banks)]
        else:
            threads = [ThreadWithResult(target=document_write, args=[qn_all[i], i]) for i in range(total_sets_needed)] 

        [i.start() for i in threads]

if __name__ == '__main__':
    main(home_link, page_link, work_path, nav_keys_civil, syllabus_civil, nav_keys_sub, syllabus_sub)
