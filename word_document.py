from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from code import qn_all

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

total_questions = len(qn_all)
option_numbers = ['a', 'b', 'c', 'd', 'e', 'f']

st = 'a'
for i in range(total_questions):
    question = qn_all[i][0]
    options = qn_all[i][1]
    answer = int(options[-1])
    options = options[:-1]
    total_options = len(options)
    writedocx(f'{i+1}. {question}', style = st)
    st += 'a'
    for j in range(total_options):
        # print(j, ', ', answer, '\n')
        if j == answer:
            writedocx(f'    {option_numbers[j]}. {options[j]}', font_bold=True, style=st)
        else:
            writedocx(f'    {option_numbers[j]}. {options[j]}', style=st)
        st += 'a'    
document.save('word.docx')