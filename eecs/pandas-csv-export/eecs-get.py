#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

#url = "http://catalog.mit.edu/subjects/6/"

#driver = webdriver.Chrome()
#driver.get(url)

#page_source = driver.page_source
#mit_page = open("mit_page.txt", "a")
#mit_page.write(page_source)
#mit_page.close()

from bs4 import BeautifulSoup as bs
import csv

mit_page = open("mit_eecs.html", "r")
soup = bs(mit_page, "lxml")

# Create csv
mit_csv = open('mit_eecs.csv', 'w', newline='')
writer = csv.writer(mit_csv)

header = ['course_title', 'course_code', 'prereq_courses', 'same_subjects', 'course_desc']
writer.writerow(header)

for element in soup.find_all(class_="courseblock"):
    course_title = element.find(class_="courseblocktitle").text
    course_code = course_title.split(" ")[0]
    
    prereq_block = element.find(class_="courseblockprereq")
    prereq_desc = prereq_block.text
    prereq_courses = []
    for prereq_course in prereq_block.find_all("a"):
        prereq_courses.append(prereq_course["href"].strip('/search/?P='))
       
    same_subjects = []  
    course_block_cluster = element.find(class_="courseblockcluster")
    if course_block_cluster: # to catch NoneType
        for line in course_block_cluster.text.splitlines(): # to filter out Same Subject as from Subject meets with
            if "Same subject as" in line:
                same_subjects = line.strip("Same subject as").split(', ')
                    
    course_desc = element.find(class_="courseblockdesc").text    

    row = [course_title, course_code, prereq_courses, same_subjects, course_desc]
    writer.writerow(row)
    print(row)
