# TODO: handle prerequisites better
# clusters like Calculus II (GIR) 18.02|18.02A|18.022|18.024
# AND and OR statements like Physics II (GIR), 16.001, and (18.03 or 18.032)
# coreqs and prereqs

# TODO: add column for course department

import requests
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd

# Get urls for each subject
urls = []

subjects_url = "http://catalog.mit.edu/subjects/#bycoursenumbertext"
subjects_html = requests.get(subjects_url).text
subjects_soup = bs(subjects_html, "html.parser")

notinpdf = subjects_soup.find("div", {"class":"notinpdf"})
for subject in notinpdf.find_all("a"):
    url = subject["href"]
    urls.append(f"http://catalog.mit.edu{url}")
    
courses_df = pd.DataFrame(columns=['course_title', 'course_code', 'prereq_desc', 'same_subjects', 'course_desc'])
prereqs_df = pd.DataFrame(columns=['course_code', 'prereq_code'])

for url in urls:
    request = requests.get(url)
    html = request.text
    soup = bs(html, "lxml")
    
    for element in soup.find_all(class_="courseblock"):
        
        # TITLE
        course_block_title = element.find(class_="courseblocktitle").text
        course_title = " ".join(course_block_title.split(" ")[1:]) 
        course_code = course_block_title.split(" ")[0] # Also captures COURSE_CODE1,\xa0COURSE_CODE12
        
        # PREREQS
        prereq_block = element.find(class_="courseblockprereq")
        
        prereq_desc = ""
        try: 
            prereq_desc = prereq_block.text.strip(" ")
        except AttributeError:
            pass
            
        prereq_courses = []
        try: 
            for prereq_code in prereq_block.find_all("a"):
                prereq_courses.append(prereq_code["href"].strip('/search/?P='))
        except AttributeError:
            pass
        
        # CLUSTERS
        course_block_cluster = element.find(class_="courseblockcluster")

        same_subjects = []  
        if course_block_cluster: # to catch NoneType
            for line in course_block_cluster.text.splitlines(): # to filter out "Same Subject As" from "Subject Meets With"
                if "Same subject as" in line:
                    same_subjects = line.strip("Same subject as").split(', ')
        
        # DESCRIPTION
        course_desc = element.find(class_="courseblockdesc").text.strip(" ")
        
        course_row = [course_title, course_code, prereq_desc, same_subjects, course_desc]
        courses_df.loc[len(courses_df)] = course_row
        
        for prereq_code in prereq_courses: 
            prereq_row = [course_code, prereq_code]
            prereqs_df.loc[len(prereqs_df)] = prereq_row

courses_df.to_json('./data/nodes.json', orient='records')
prereqs_df.to_json('./data/links.json', orient='records')