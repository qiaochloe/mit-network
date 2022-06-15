import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from department_names import department_names


def scrape_courses():
    # Get urls for each subject
    urls = []

    subjects_url = "http://catalog.mit.edu/subjects/#bycoursenumbertext"
    subjects_html = requests.get(subjects_url).text
    subjects_soup = bs(subjects_html, "html.parser")

    notinpdf = subjects_soup.find("div", {"class": "notinpdf"})
    for subject in notinpdf.find_all("a"):
        url = subject["href"]
        urls.append(f"http://catalog.mit.edu{url}")

    courses_df = pd.DataFrame(
        columns=[
            "course_title",
            "course_code",
            "prereq_desc",
            "same_subjects",
            "course_desc",
        ]
    )
    prereqs_df = pd.DataFrame(columns=["course_code", "prereq_code"])

    for url in urls:
        request = requests.get(url)
        html = request.text
        soup = bs(html, "lxml")

        for element in soup.find_all(class_="courseblock"):

            # TITLE
            course_block_title = element.find(class_="courseblocktitle").text
            course_title = " ".join(course_block_title.split(" ")[1:])
            course_code = course_block_title.split(" ")[
                0
            ]  # Also captures COURSE_CODE1,\xa0COURSE_CODE12

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
                    prereq_courses.append(prereq_code["href"].strip("/search/?P="))
            except AttributeError:
                pass

            # CLUSTERS
            course_block_cluster = element.find(class_="courseblockcluster")

            same_subjects = []
            if course_block_cluster:  # to catch NoneType
                for (
                    line
                ) in (
                    course_block_cluster.text.splitlines()
                ):  # to filter out "Same Subject As" from "Subject Meets With"
                    if "Same subject as" in line:
                        same_subjects = line.strip("Same subject as").split(", ")

            # DESCRIPTION
            course_desc = element.find(class_="courseblockdesc").text.strip(" ")

            course_row = [
                course_title,
                course_code,
                prereq_desc,
                same_subjects,
                course_desc,
            ]
            courses_df.loc[len(courses_df)] = course_row

            for prereq_code in prereq_courses:
                prereq_row = [course_code, prereq_code]
                prereqs_df.loc[len(prereqs_df)] = prereq_row

    # courses_df.to_json('./website/data/nodes.json', orient='records')
    # prereqs_df.to_json('./website/data/links.json', orient='records')

    return courses_df, prereqs_df


def add_department_attribute():
    def get_department_code(course_code):
        return course_code.split(".")[0]

    department_names
    department_codes = courses_df["course_code"].apply(get_department_code).unique()
    department_dict = dict(zip(department_codes, department_names))

    # def get_department(course_code):
    #    department_code = get_department_code(course_code)
    #    department = department_dict[department_code]
    #    return department

    # Add department attribute to courses_df
    department = courses_df["course_code"].apply(
        lambda course_code: department_dict[get_department_code(course_code)]
    )
    department = department.rename("course_department")
    courses_df = courses_df.merge(department, left_index=True, right_index=True)

    # Create departments_df
    departments_df = pd.DataFrame(
        {"department_code": department_codes, "department_name": department_names}
    )

    # courses_df.to_json("./website/data/nodes.json", orient="records")
    # departments_df.to_json("./website/data/departments.json", orient="records")

    return courses_df, departments_df
