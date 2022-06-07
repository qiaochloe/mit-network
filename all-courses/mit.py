import requests
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd

#major_num = [i for i in range(1, 25) if i not in [13, 19, 23]]

#for i in major_num:
#    url = f"http://student.mit.edu/catalog/m{i}a.html"
    
#    request = requests.get(url).text
#    soup = bs(request, "html.parser")

#    # Count number of pages in course section
#    contentmini = soup.find(id="contentmini")
#    td = contentmini.find_all("td")
#    num_pages = 0
#    for x in td:
#        num_pages += 1
#    num_pages = int((num_pages - 3)/2)

#    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
#    for x in range(0, num_pages):
#        urls.append(f"http://student.mit.edu/catalog/m{i}{abc[x]}.html")

# Get urls for each subject
urls = []

subjects_url = "http://catalog.mit.edu/subjects/#bycoursenumbertext"
subjects_html = requests.get(subjects_url).text
subjects_soup = bs(subjects_html, "html.parser")

notinpdf = subjects_soup.find("div", {"class":"notinpdf"})
for subject in notinpdf.find_all("a"):
    url = subject["href"]
    urls.append(f"http://catalog.mit.edu{url}")
    
# Create MIT csv and set header
mit_csv = open('mit.csv', 'w', newline='')
writer = csv.writer(mit_csv)

header = ['course_title', 'course_code', 'prereq_courses', 'same_subjects', 'course_desc']
writer.writerow(header)

for url in urls:
    request = requests.get(url)
    html = request.text
    soup = bs(html, "lxml")
    
    for element in soup.find_all(class_="courseblock"):
        course_title = element.find(class_="courseblocktitle").text
        course_code = course_title.split(" ")[0]
        
        prereq_block = element.find(class_="courseblockprereq")
        
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

        same_subjects = []  
        course_block_cluster = element.find(class_="courseblockcluster")
        if course_block_cluster: # to catch NoneType
            for line in course_block_cluster.text.splitlines(): # to filter out Same Subject as from Subject meets with
                if "Same subject as" in line:
                    same_subjects = line.strip("Same subject as").split(', ')
                        
        course_desc = element.find(class_="courseblockdesc").text
        
        row = [course_title, course_code, prereq_courses, same_subjects, course_desc]
        writer.writerow(row)
        
