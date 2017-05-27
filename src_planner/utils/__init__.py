"""
Some tools that we use
"""
import re
import json
from flask import current_app as app

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def parse_info(text):
    text = text.decode('utf-8')
    #collapses the newlnes
    text = re.sub(r'\n+', '\n', text).splitlines()

    info_start = text.index('Student Information')
    info_end = text.index('University Requirements')

    #gets your major
    major_index = text.index('Major:')+1
    major = text[major_index]

    #gets admit date and name
    admit_date = ""
    name = ""
    uid = "XXXXXXXX"
    for line in text[info_start:info_end]:
        admit_date = line if re.search(r'\d+/\d+/\d+', line) else admit_date
        # name = line if re.search(r'[A-Z]+, ([A-Z]| )+$', line) else name
        uid = line if re.search(r'\d{9}', line) else uid
        if not name and ',' in line:
            name = line

    #gets the classes taken
    classes_by_quarter = {}
    current_quarter = ''
    for line in text[info_end:]:
        if 'Quarter' in line:
            if current_quarter and current_quarter not in classes_by_quarter:
                classes_by_quarter[current_quarter] = (None, )
            current_quarter = line
        elif current_quarter and re.search(r'[A-Z]+ [A-Z]*\d+[A-Z]*', line) and line.count(' ') < 4:
            if current_quarter in classes_by_quarter:
                classes_by_quarter[current_quarter] = classes_by_quarter[current_quarter] + (line, )
            else:
                classes_by_quarter[current_quarter] = (line, )


    user = {
        'name': name,
        'uid': uid,
        'major': major,
        'admit_date': admit_date,
        'classes_by_quarter' : classes_by_quarter
       }    
    return json.dumps(user)
