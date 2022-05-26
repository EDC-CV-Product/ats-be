import os

from django.forms import GenericIPAddressField
from matplotlib.pyplot import text
from . import utils
import spacy
import pycountry
import pprint
from spacy.matcher import Matcher
import multiprocessing as mp

'''class Job_disc(object):
    def __init__(self, Job_disc):

        self.__Job_disc      = Job_disc
        self.__text_raw    = utils.extract_text(self.__Job_disc, os.path.splitext(self.__Job_disc)[1])
        self.__text        = ' '.join(self.__text_raw.split())
        self.__text_disc   = utils.clean_job_decsription(self.__text)

        return'''

class ResumeParser(object):
    def __init__(self, resume):
        nlp = spacy.load('en_core_web_lg')
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name'              : None,
            'email'             : None,
            'mobile_number'     : None,
            'skills'            : None,
            'education'         : None,
            'experience'        : None,
            'summary'           : None,
            # 'zip_code'          : None,
            # 'country'           : None,
            # 'city'              : None,
            # 'training_certificate' : None,
            #'competencies'      : None,
            #'measurable_results': None
        }

        self.__resume      = resume
        self.__text_raw    = utils.extract_text(self.__resume, os.path.splitext(self.__resume)[1])
        self.__text        = ' '.join(self.__text_raw.split())
        self.__text_clean  = utils.clean_text(self.__text)
        self.__text_clean1 = utils.remove_punctuation(self.__text_clean) 
        self.__text_clean2 = utils.text_treatment(self.__text_clean1)    
        self.__nlp         = nlp(self.__text)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        summary    = utils.extract_summary(self.__text)
        zip_code   = utils.extract_zipcode(self.__text)
        country    = utils.extract_country(self.__text)
        city       = utils.extract_city(self.__text)
        training_certificate = utils.extract_training(self.__text)
        name       = utils.extract_name(self.__text)
        email      = utils.extract_email(self.__text)
        mobile     = utils.extract_mobile_number(self.__text)
        skills     = utils.extract_skills(self.__nlp, self.__noun_chunks)
        edu        = utils.extract_education(self.__text) # [sent.text.strip() for sent in self.__nlp.sents]
        experience = utils.extract_experience(self.__text)
        total_experience = utils.get_experience(self.__text_clean2)
        entities   = utils.extract_entity_sections(self.__text_raw)
        #scoring = utils.process_files(self.__text, self.__text_disc)
        #self.__details['scoring'] = scoring
        self.__details['name'] = name
        self.__details['email'] = email
        self.__details['mobile_number'] = mobile
        self.__details['skills'] = skills
        self.__details['summary'] = summary
        self.__details['zip_code'] = zip_code
        self.__details['country'] = country
        self.__details['city'] = city
        self.__details['training_certificate'] = training_certificate
        #self.__details['education'] = entities['Education']
        self.__details['education'] = edu
        self.__details['experience'] = experience
        self.__details['total_experience'] = total_experience
        try:
            self.__details['competencies'] = utils.extract_competencies(self.__text_raw, entities['experience'])
            self.__details['measurable_results'] = utils.extract_measurable_results(self.__text_raw, entities['experience'])
        except KeyError:
            self.__details['competencies'] = []
            self.__details['measurable_results'] = []
        return

def resume_result_wrapper(resume):
        parser = ResumeParser(resume)
        return parser.get_extracted_data()

'''
class Job_disc(object):
    def __init__(self, Job_disc):

        self.__Job_disc      = Job_disc
        self.__text_raw    = utils.extract_text(self.__Job_disc, os.path.splitext(self.__Job_disc)[1])
        self.__text        = ' '.join(self.__text_raw.split())
        self.__text_disc   = utils.clean_job_decsription(self.__text)

        return'''



if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [pool.apply_async(resume_result_wrapper, args=(x,)) for x in resumes]

    results = [p.get() for p in results]

    pprint.pprint(results)

