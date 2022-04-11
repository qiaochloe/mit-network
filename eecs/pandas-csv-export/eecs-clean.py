import pandas as pd
import numpy as np

df = pd.read_csv('eecs/og-eecs.csv')

# Drop columns
to_drop = ["same_subjects", "course_desc"]
df.drop(to_drop, inplace=True, axis=1)

# Remove course_code in course_title
# Remove "" in course_title
count = 0
for course in df['course_title']:
    course = course.strip('\"')        
    course = course.split(' ') 
    course =  " ".join(course[1:])
    df.iat[count, 0] = course
    count += 1
 
# Remove courses that show up more than two times
ununique = df['course_title'].value_counts()
ununique = ununique[ununique > 2]
ununique = ununique.keys().tolist()

for course in ununique:
    df = df.drop(df[df["course_title"] == course].index)

# Clean prereq_courses; turn to list
codes = df["course_code"].tolist()
count = 0

for prereqs in df["prereq_courses"]:
    prereqs = prereqs.strip('][').split(', ')

    temp = []
    for prereq in prereqs:
        prereq = prereq.strip("\'").split("|")
        temp.extend(prereq)
    
    prereq = [req for req in temp if req in codes]
    df.iat[count,2] = prereq
    
    count += 1
        
df.to_csv('eecs/eecs.tsv', sep="\t", index=False)