import re
import json


def get_info(text):

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
    for line in text[info_start:info_end]:
        admit_date = line if re.search(r'\d+/\d+/\d+', line) else admit_date
        # name = line if re.search(r'[A-Z]+, ([A-Z]| )+$', line) else name
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
        'major': major,
        'admit_date': admit_date,
        'classes_by_quarter' : classes_by_quarter
       }    
    return json.dumps(user)
