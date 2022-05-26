import textract
import re

def clean_job_decsription(jd):
    # Lower
    clean_jd = jd.lower()
    
    clean_jd = clean_jd.strip()
    
    # replace multiple space with single space
    clean_jd = re.sub('\r+',' ',clean_jd)
    clean_jd = re.sub('\n+',' ',clean_jd)
    clean_jd = re.sub('\s+',' ',clean_jd)
    
    return(clean_jd)


def get_content_as_string(filename):
    text = textract.process(filename)
    # creating an object 

    lower_case_string =  text.decode('utf-8').lower()

    #lower_case_string = re.sub('[^a-zA-Z0-9 \n]', '', lower_case_string)

    lower_case_string = clean_job_decsription(lower_case_string)

    return lower_case_string

def get_content_as_string_jobdisc(filename):
    text = textract.process(filename)
    lower_case_string =  str(text.decode('utf-8')).lower()
    final_string = re.sub('[^a-zA-Z0-9 \n]', '', lower_case_string)
    return lower_case_string