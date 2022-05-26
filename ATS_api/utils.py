import io
import sys
import os
import re
import glob
from pathlib import PurePath
import pandas as pd
import spacy
import operator
import datefinder

from preprocessing import docx_processing  as doc, textract_processing as txt
from text_processing import tf_idf_cosine_similarity as tf_idf,doc2vec_comparison as d2v
from text_processing import cv_cosine_similarity as cv
from text_processing import tf_idf_cosine_similarity as tf_idf

from . import constants as cs
from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

#Docx resume
import docx2txt
import pycountry
from geotext import GeoText
# nltk
import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
set(stopwords.words('english'))

stop = stopwords.words('english')

'''# sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import docx_processing  as doc, textract_processing as txt
from text_processing import tf_idf_cosine_similarity as tf_idf,doc2vec_comparison as d2v
from text_processing import cv_cosine_similarity as cv'''

#from src.info_extractor import InfoExtractor
from typing import *
from dateutil.relativedelta import relativedelta
# from ResumeRater.src.utils import loadDocumentIntoSpacy, countWords, loadDefaultNLP
from typing import *

def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files
    :param pdf_path: path to PDF file to be extracted
    :return: iterator of string of extracted text
    '''
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()

def read_pdf_resume(pdf_doc):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_doc, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True,check_extractable=True):           
            page_interpreter.process_page(page)     
            text = fake_file_handle.getvalue() 
        # close open handles      
        converter.close() 
        fake_file_handle.close() 
        if text:     
            return text

def extract_text_from_doc(doc_path):
    '''
    Helper function to extract plain text from .doc or .docx files
    :param doc_path: path to .doc or .docx file to be extracted
    :return: string of extracted text
    '''
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)


def extract_text(file_path, extension):
    '''
    Wrapper function to detect the file extension and call text extraction function accordingly
    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == '.pdf':
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page
    elif extension == '.docx' or extension == '.doc':
        text = extract_text_from_doc(file_path)
    return text


def extract_entity_sections(text):
    '''
    Helper function to extract all the raw text from sections of resume
    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    # sections_in_resume = [i for i in text_split if i.lower() in sections]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    
    # entity_key = False
    # for entity in entities.keys():
    #     sub_entities = {}
    #     for entry in entities[entity]:
    #         if u'\u2022' not in entry:
    #             sub_entities[entry] = []
    #             entity_key = entry
    #         elif entity_key:
    #             sub_entities[entity_key].append(entry)
    #     entities[entity] = sub_entities

    # pprint.pprint(entities)

    # make entities that are not found None
    # for entity in cs.RESUME_SECTIONS:
    #     if entity not in entities.keys():
    #         entities[entity] = None 
    return entities
def extract_summary(text):

    exp = re.findall(r"(?:summary:(.+?)technical skills|skills:)+", text)
    exp = ''.join(str(e) for e in exp)

    return exp

def extract_training(text):
    certif = re.findall(r"(?:training and certificates:|certificates:|training:(.+?)work experience:)+", text)
    training = ''.join(str(e) for e in certif)

    return training

def extract_zipcode(text):
    zipp = re.findall('(?<!\n)[\d]{5,6}[\-]?[\d]*', text)
    zipp = ''.join(str(e) for e in zipp)

    return zipp

def extract_country(text):

    for country in pycountry.countries:
        if country.name in text:
            return country.name

def extract_city(text):
    cities = GeoText(text)
    return cities

'''def extract_mobile_number(text):
    
    Helper function to extract mobile number from text
    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    
    # Found this complicated regex on : https://zapier.com/blog/extract-links-email-phone-regex/
    
    phone = re.findall(re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?"), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 11:
            return '+' + number
        else:
            return '''

def extract_mobile_number(document):
    #This function has to be further modified better and accurate results.
    #Possible phone number formats - Including +91 or just with the numbers.
    
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{5}[-\.\s]??\d{4})'''

    pattern = re.compile(mob_num_regex)
    matches = []
    for line in document:
        match = pattern.findall(line)
        for mat in match:
            # if len(mat) > 12:
            matches.append(mat)

    return matches


def extract_email(text):
    '''
    Helper function to extract email id from text
    :param text: plain text extracted from resume file
    '''
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

from spacy import *
nlp = spacy.load('en_core_web_lg')
matcher = Matcher(nlp.vocab)

'''def extract_name(nlp_text, matcher):
    
    Helper function to extract name from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    

    pattern = [cs.NAME_PATTERN]
    
    matcher.add('NAME', pattern, on_match=on_match)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text'''


def extract_name(text):
    person_names = []

    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))
    return person_names

'''def extract_name(text):

    person_name = []
    
    splitted=text.split()
    first = splitted[0]
    last = splitted[1]
    name = first +" "+ last
    person_name.append(name)

    return person_name'''


def extract_skills(nlp_text, noun_chunks):
    '''
    Helper function to extract skills from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def clean_job_decsription(jd):

    ''' a function to create a word cloud based on the input text parameter'''
    ## Clean the Text
    # Lower
    clean_jd = jd.lower()
    
    # remove punctuation
    #clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
    
    # remove trailing spaces
    clean_jd = clean_jd.strip()
    
    # replace multiple space with single space
    
    clean_jd = re.sub('\s+',' ',clean_jd)
    
    # remove numbers
    # clean_jd = re.sub('[0-9]+', '', clean_jd)
    
    # tokenize 
    #clean_jd = clean_jd.split(' ')
    
    # remove stop words
    #stop = stopwords.words('english')
    #clean_jd = [w for w in clean_jd if not w in stop]
    
    #clean_jd = (''.join(clean_jd))
    
    return(clean_jd)


def clean_fields(jd):

    ## Clean the Text
    # Lower
    clean_jd = jd.lower()
    
    # remove punctuation
    clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
    
    # remove trailing spaces
    clean_jd = clean_jd.strip()
    
    # replace multiple space with single space
    
    clean_jd = re.sub('\s+',' ',clean_jd)
    
    # remove numbers
    # clean_jd = re.sub('[0-9]+', '', clean_jd)
    
    # tokenize 
    #clean_jd = clean_jd.split(' ')
    
    # remove stop words
    #stop = stopwords.words('english')
    #clean_jd = [w for w in clean_jd if not w in stop]
    
    #clean_jd = (''.join(clean_jd))
    
    return(clean_jd)

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()


def clean_text(text):
    '''
    Removes new line and unwanted page of values from the text
    '''
    text1 = re.compile('[%s]' % '(\\n)*(\\x0c)*').sub(' ', text)  
    text2 = re.compile(r'Page [0-9]+ of [0-9]+').sub(' ', text1)  
    return text2

def remove_punctuation(text):
    '''
    Removes punctuation
    Did not remove few characters such as .,$%-~:;?!
    '''
    clean_punct =  re.compile('[%s]' % re.escape('"#&\()*+/<=>@[\\]^_{|}')).sub(' ', text) 
    return clean_punct

def text_treatment(text):
    '''
    Replacing unwanted characters with space
    '''
    text = text.replace("\x00", '').replace("\x01", '').replace("\x02", '').replace("\x03", '') \
    .replace("\x04", '').replace("\x05", '').replace("\x06", '').replace("\x07", '').replace("\x08", '') \
    .replace("\x0e", '').replace("\x11", '').replace("\x12", '').replace("\x10", '').replace("\x19", '') \
    .replace("\x1b", '').replace("\x14", '').replace("\x15", '').replace('/', '').replace('=', '').replace("〓", "") \
    .replace("»", "").replace("«", "").replace("¬", "").replace('`', '').replace("•", "").replace("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬","")\
    .replace("”", "").replace("§", "").replace("¨", "").replace("©", "").replace("›", "").replace("■", "").replace("ifttt", "")\
    .replace("→", "").replace("⇨", "").replace("∎", "").replace("√", "").replace("□", "").replace("~~~", "").replace("★", "")\
    .replace("*", "").replace("&", "").replace("►", "").replace("◊", "").replace("☞", "").replace("#", "")\
    .replace("❖", "").replace("➠", "").replace("➢", "").replace("", "").replace("✓", "").replace("--","") \
    .replace("√", "").replace("✔", "").replace("♦", "").replace("◦", "").replace("●", "").replace("▫", "")\
    .replace("▪", "").replace("…", "").replace("þ", "").replace("®", "").replace('', '').replace("...", "")
    return text

def masters(text):
    '''
    Filtering people who have a Masters/PhD degree with value 1 from the Education column
    '''
    patterns = re.compile("(Master's|Master|M.S.|MS|M.Sc.|MSc|PhD|Ph.D.|Honors)")
    #print('Looking for "%s" in "%s" ->' % (patterns, text))
    if patterns.search(text):
        value = 1
    else:
        value = 0
    return value

def get_experience(text):
    text1 =  re.findall(r"([a-zA-Z]+\s\d+\s-\s\D+\s\d*\s\s?)(\d+\syears?\s\d+ months?|\d+ years?|\d+ months?)",text)
    '''
    text1: Finding strings of pattern 'June 2011 - December 2012  ', '1 year 7 months'
    Finding the total experience of a person
    '''
    years = 0
    months= 0 
    for i in text1:
        match_years = re.search("[0-9]+\syears?",i[1])     # to get all the years
        if match_years != None:
            yr = int(match_years.group()[0])
            years += yr
        match_months = re.search("[0-9]+\smonths?",i[1])   # to get all the months
        if match_months != None:
            month = int(match_months.group()[0:2])
            months += month
    total_exp = round(years + (months/12),2)
    return total_exp

def Get_contact(text):
    '''
    Filtering the Contact column to get any piece of contact information such as Email or Github or Phone number 
    '''
    if re.findall(r'[a-zA-Z0-9.-]+@[a-zA-Z-]+\.com+', text):
        value = re.findall(r'[a-zA-Z0-9.-]+@[a-zA-Z-]+\.com+', text)[0]
    elif re.findall(r'github\.com/\s?[a-zA-Z0-9_]+', text):
        value = re.findall(r'github\.com/\s?[a-zA-Z0-9_]+', text)[0]
    elif re.findall(r'\d{3}-\d{3}-\d{4}', text):
        value = re.findall(r'\d{3}-\d{3}-\d{4}', text)[0]
    else:
        value = None    
    return value

def process_files(req_document,resume_docs):
    
    # req_doc_text = doc.get_content_as_string(req_document)
    # resume_doc_text = []

    # for doct in resume_docs:
    #     resume_doc_text.append(doc.get_content_as_string(doct))

    req_doc_text = txt.get_content_as_string_jobdisc(req_document)
    # print('The start' * 5)
    resume_doc_text = []
    for doct in resume_docs:
        resume_doc_text.append(txt.get_content_as_string(doct))


    # TF-IDF - cosine similarity
    final_doc_rating_list = []
    cos_sim_list = tf_idf.get_tf_idf_cosine_similarity(req_doc_text,resume_doc_text)
    final_doc_rating_list = []
    zipped_docs = zip(cos_sim_list,resume_docs)
    sorted_doc_list = sorted(zipped_docs, key = lambda x: x[0], reverse=True)
    
    for element in sorted_doc_list:
        doc_rating_list = []
        doc_rating_list.append(os.path.basename(element[1]))
        doc_rating_list.append("{:.0%}".format(element[0]))
        final_doc_rating_list.append(doc_rating_list)

    return final_doc_rating_list


'''def extract_education(nlp_text):
    
    Helper function to extract education from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year if found else only returns education degree
    
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education'''

'''def extract_education(resume_text):
    nlp_text = nlp(resume_text)
    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        #print(index, text), print('-'*50)
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            #print(tex)

            if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]
                #print(edu.keys())

    return edu'''


'''def extract_education(resume_text):
  # regex = re.compile(r"(B\.Tech|MSc).*?(?<=-)\s+(\d+)")
  # match = regex.match(resume_text)
  list123 = []
  for i in cs.EDUCATION:
    reg = "(" + re.escape(i) + ").*?(?<=-)\s+(\d+)"
    regex = re.compile(reg, flags=re.M | re.IGNORECASE)
    for mat in regex.findall(resume_text):
      list123.append(mat)
  return list123 '''


def extract_education(document):
    
    education_terms = [term for term in cs.EDUCATION]
    education = []
    for line in document:
        for word in line.split(' '):
            if len(word) > 1 and word in education_terms:
                if line not in education:
                    education.append(line)
    #print (education)
    return (education)


def extract_experience(resume_text):
    '''
    Helper function to extract experience from resume text
    :param resume_text: Plain resume text
    :return: list of experience
    '''
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization 
    word_tokens = nltk.word_tokenize(resume_text)

    # remove stop words and lemmatize  
    filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words] 
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)
    
    # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
    #     print(i)
    
    test = []
    
    for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    return x

def extract_competencies(text, experience_list):
    '''
    Helper function to extract competencies from resume text
    :param resume_text: Plain resume text
    :return: dictionary of competencies
    '''
    experience_text = ' '.join(experience_list)
    competency_dict = {}

    for competency in cs.COMPETENCIES.keys():
        for item in cs.COMPETENCIES[competency]:
            if string_found(item, experience_text):
                if competency not in competency_dict.keys():
                    competency_dict[competency] = [item]
                else:
                    competency_dict[competency].append(item)
    
    return competency_dict

def extract_measurable_results(text, experience_list):
    '''
    Helper function to extract measurable results from resume text
    :param resume_text: Plain resume text
    :return: dictionary of measurable results
    '''

    # we scan for measurable results only in first half of each sentence
    experience_text = ' '.join([text[:len(text) // 2 - 1] for text in experience_list])
    mr_dict = {}

    for mr in cs.MEASURABLE_RESULTS.keys():
        for item in cs.MEASURABLE_RESULTS[mr]:
            if string_found(item, experience_text):
                if mr not in mr_dict.keys():
                    mr_dict[mr] = [item]
                else:
                    mr_dict[mr].append(item)
    
    return mr_dict

def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


def extract_experience(resume_text):

    '''
    Helper function to extract experience from resume text

    :param resume_text: Plain resume text
    :return: list of experience
    '''
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

# word tokenization 
    word_tokens = nltk.word_tokenize(resume_text)

# remove stop words and lemmatize  
    filtered_sentence = [w for w in word_tokens if not w in stop_words and 
    wordnet_lemmatizer.lemmatize(w) not in stop_words] 
    sent = nltk.pos_tag(filtered_sentence)


# parse regex

    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)

# for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
#     print(i)

    test = []

    for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):

        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

        # Search the word 'experience' in the chunk and then print out the text after it
        x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]

        return x