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
    
# Create csv and set header
#courses_csv = open('courses.csv', 'w', newline='')
#courses_writer = csv.writer(courses_csv)

#prereqs_csv = open('prereqs.csv', 'w', newline='')
#prereqs_writer = csv.writer(prereqs_csv)

#header = ['course_title', 'course_code', 'prereq_courses', 'same_subjects', 'course_desc']
#writer.writerow(header)

courses_df = pd.DataFrame(columns=['course_title', 'course_code', 'same_subjects', 'course_desc'])
prereqs_df = pd.DataFrame(columns=['course', 'prereq'])

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
            prereq_desc = prereq_block.text 
        except AttributeError:
            prereq_desc = "None"
            
        prereq_courses = []
        try: 
            for prereq_course in prereq_block.find_all("a"):
                prereq_courses.append(prereq_course["href"].strip('/search/?P='))
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
        
        course_row = [course_title, course_code,same_subjects, course_desc]
        courses_df.loc[len(courses_df)] = course_row
        
        for prereq in prereq_courses: 
            prereq_row = [course_code, prereq]
            prereqs_df.loc[len(prereqs_df)] = prereq_row
            
        #writer.writerow(row)

#courses_df.to_csv(file_name, encoding='utf-8')
#prereqs_df.to_csv(file_name, encoding='utf-8')

courses_df.to_json('all-courses/nodes.json', orient='records')
prereqs_df.to_json('all-courses/links.json', orient='records')