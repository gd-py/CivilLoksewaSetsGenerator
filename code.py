page_link = "https://www.indiabix.com/civil-engineering/"
working_dir = "C:\\Users\\Irthak Miisaaz\\OneDrive - Tribhuvan University\Desktop\\civil sets\Without explanations - old\\"

## engineer
nav_keys_civil = ["theory-of-structures", "strength-of-materials", "surveying", "building-materials", "concrete-technology", "soil-mechanics-and-foundation-engineering", "construction-management", "estimating-and-costing", "engineering-economy"]
syllabus_civil = [3, 2, 7, 6, 5, 6, 6, 5, 4, 3, 3]
## sub-engineer
nav_keys_sub = ["surveying", "building-materials", "theory-of-structures", "strength-of-materials", "hydraulics", "soil-mechanics-and-foundation-engineering", "rcc-structures-design", "building-construction", "concrete-technology", "water-supply-engineering", "waste-water-engineering", "irrigation", "highway-engineering", "estimating-and-costing", "construction-management", "airport-engineering"]
syllabus_sub = [4, 4, 2, 2, 4, 4, 4, 2, 2, 2, 2, 4, 4, 4, 4, 2]

for_civil = True
create_question_bank = False
test_phase = True
write_to_document = False
total_sets_needed = 1
if test_phase: total_sets_needed = 5

if for_civil:
    nav_keys = nav_keys_civil
    syllabus = syllabus_civil
else:
    nav_keys = nav_keys_sub
    syllabus = syllabus_sub


from bs4 import BeautifulSoup
import requests
from requests.models import HTTPError
import re
import random
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import time, sys
from threading_self import ThreadWithResult

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

            qn_temp = [[a.text] for a in soup.find_all('td', class_="bix-td-qtxt")]
            
            opts_ids = [a['id'].split('_')[-1] for a in soup.find_all("table", class_= "bix-tbl-options")]
            opts = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            ans_list = [a.text for a in soup.find_all("span", class_=re.compile(r'jq-hdnakqb.*'))]

            # opts_description = []
            for k, l in enumerate(opts_ids):
                opts_temp = [a.text for a in soup.find_all('td', id=re.compile(rf'tdOptionDt...{l}'))]
                opts_temp.append(opts.index(ans_list[k]))
                # opts_description.append(opts_temp)
                qn_temp[k].append(opts_temp)

            qens.append(qn_temp)
    qn_subwise = []
    for i in qens:
        for j in i:
            qn_subwise.append(j)
    
    ########### filters here! #############
    # filter out questions containing empty options
    temp_qn_subwise = qn_subwise
    for j in temp_qn_subwise:
        if '' in j[1]:
            # print(qn_subwise[i])
            # print('\n')
            qn_subwise.remove(j)
            # if nav_keys[index] == 'strength-of-materials':
            #     print(j)

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
            qn_subwise.remove(j)

    # Again filter out questions containing empty options
    for j in qn_subwise:
        if '' in j[1]:
            # print(qn_subwise[i])
            # print('\n')
            qn_subwise.remove(j)
            # if nav_keys[index] == 'strength-of-materials':
            #     print(j)

    # filter out questions containing figures or indian datas.    
    for j in qn_subwise:
        if 'below figure' in j[0] or 'given figure' in j[0] or 'India' in j[0] or 'india' in j[0]:
            qn_subwise.remove(j)

    # filter out questions with options that are incomplete(end with '=') due to presence of math formulas.
    for j in qn_subwise:
        for k in j[1]:
            if k and type(k) == str and k[-1] == '=':
                print(j)
                qn_subwise.remove(j)
                break

    ############# end of filters! #############

    return qn_subwise
    
# fetch questions from text file for dwaring and professional practice
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
def document_write(qn_all, bank_no):
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

    def writedocx(content, font_name = 'Times New Roman', font_size = 11, font_bold = False, font_italic = False, font_underline = False, color = RGBColor(0, 0, 0),
                before_spacing = 0, after_spacing = 8, line_spacing = 1.08, keep_together = False, keep_with_next = False, page_break_before = False,
                widow_control = True, align = 'left', style = ''):
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
        # if i+1 <= 40:
        writedocx(f'{i+1}. {question}', style = st)
        # else:    
            # writedocx(f'{i+5}. {question}', style = st)
        st += 'a'
        for j in range(total_options):
            # print(j, ', ', answer, '\n')
            if j == answer:
                # if bank_no == 0:
                #     print([i, j], '\n')
                writedocx(f'    {option_numbers[j]}. {options[j]}', font_bold=True, style=st)
                st += 'b'
            else:
                # pass
                try:
                    writedocx(f'    {option_numbers[j]}. {options[j]}', font_bold=False, style=st)
                except:
                    print(bank_no, end=' ')
                    print(option_numbers, j, options, '\n')
                st += 'a'    
        if i%20 == 0:
            st_num += 1
            st = chr(st_num)
            # pass
            print('.', end='')
    
    core_properties = document.core_properties
    core_properties.author  = 'Ganesh Dhungana'
    core_properties.comments = ''
    if test_phase:
        document.save(working_dir + rf'tests\test_file{bank_no + 1}.docx')
    else:
        if not create_question_bank:
            if not for_civil:
                document.save(working_dir + rf'sets_subengineer\set_sub{bank_no + 200 - total_sets_needed + 1}.docx')    #Uncomment this for creating sets
            else:
                document.save(working_dir + rf'sets_engineer\set_{bank_no + 1}.docx')    #Uncomment this for creating sets
        else:
            if not for_civil:
                document.save(working_dir + rf'banks_sub\bank_qn[{1+sum(syllabus_sub[:bank_no])}-{sum(syllabus_sub[:bank_no+1])}].docx')    #Uncomment this for creating banks
            else:
                document.save(working_dir + rf'banks\bank_qn[{1+sum(syllabus_civil[:bank_no])}-{sum(syllabus_civil[:bank_no+1])}].docx')    #Uncomment this for creating banks

# print('fetching data ', end='')
# threads = [ThreadWithResult(target=question_fetch, args=[page_link, nav_keys, i, test_phase]) for i in range(len(nav_keys))]
threads = [1, 2, 3]
# [i.start() for i in threads]
# [i.join() for i in threads]

grand_collection = [i.result for i in threads]

if for_civil:
    drawing_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\Without explanations - old\drawing.txt"
    drawing_answer_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\Without explanations - old\drawing_answer.txt"
    drawing_questions = fetch_from_file(drawing_file, drawing_answer_file)

    print('\n\n')
    pp_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\Without explanations - old\pp.txt"
    pp_answer_file = r"C:\Users\Irthak Miisaaz\OneDrive - Tribhuvan University\Desktop\civil sets\Without explanations - old\pp_answer.txt"
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

# print('\n')
# for i, j in enumerate(grand_collection[0]):
#     print(i+1, '. ', j, '\n')

print('\nFinished fetching data!\n')

if write_to_document:
    print('Writing to document ', end='')
    if create_question_bank:
        added_banks = 0
        if for_civil:
            added_banks = 2
        threads = [ThreadWithResult(target=document_write, args=[qn_all[i], i]) for i in range(len(nav_keys)+added_banks)] # range(len(nav_keys)) for creating bank and range(total_sets_needed) for creating 100 sets
    else:
        threads = [ThreadWithResult(target=document_write, args=[qn_all[i], i]) for i in range(total_sets_needed)] # range(len(nav_keys)) for creating bank and range(total_sets_needed) for creating 100 sets

    [i.start() for i in threads]

# print('\n')
# for i, j in enumerate(qn_all[0]):
#     print(i+1, '. ', j)
#     print('\n')