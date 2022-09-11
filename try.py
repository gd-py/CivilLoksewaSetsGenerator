from docx import Document
file_names = [rf'sets_engineer\set_{i}.docx' for i in range(1, 101)]
for file_name in file_names:
    document = Document(file_name)
    for paragraph in document.paragraphs:
        if '***Sub Engineer***' in paragraph.text:
            print(paragraph.text)
            paragraph.text = '***Engineer***'
    core_properties = document.core_properties
    core_properties.author = 'Ganesh Dhungana'
    core_properties.comments = ''
    document.save(file_name)