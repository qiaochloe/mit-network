import pandas as pd

courses_df = pd.read_json("./website/data/nodes.json")

department_names = [
    "Civil and Environmental Engineering",
    "Mechanical Engineering",
    "Materials Science and Engineering",
    "Architecture",
    "Chemistry",
    "Electrical Engineering and Computer Science",
    "Biology",
    "Physics",
    "Brain and Cognitive Sciences",
    "Chemical Engineering",
    "Urban Studies and Planning",
    "Earth, Atmospheric, and Planetary Sciences",
    "Economics",
    "Management",
    "Aeronautics and Astronautics",
    "Political Science",
    "Mathematics",
    "Biological Engineering",
    "Humanities",
    "Anthropology",
    "History",
    "Global Lanugages",
    "Literature",
    "Music and Theater Arts",
    "Writing",
    "Nuclear Science and Engineering",
    "Linguistics and Philosophy",
    "Aerospace Studies",
    "Concourse Program",
    "Comparative Media Studies",
    "Computational and Systems Biology",
    "Center for Computational Science and Engineering",
    "Chief Digital Officer",
    "Edgerton Center",
    "Engineering Management",
    "Experimental Study Group",
    "Health Sciences and Technology",
    "Institute for Data, Systems and Society",
    "Media Arts and Sciences",
    "Military Science",
    "Naval Science",
    "Supply Chain Management",
    "Special Program",
    "Science, Technology, and Society",
    "Women's and Gender Studies",
]


def get_department_code(course_code):
    return course_code.split(".")[0]


department_codes = courses_df["course_code"].apply(get_department_code).unique()
department_dict = dict(zip(department_codes, department_names))


def get_department(course_code):
    department_code = get_department_code(course_code)
    department = department_dict[department_code]
    return department


# Add department attribute to courses_df
department = courses_df["course_code"].apply(get_department)
department = department.rename("course_department")
courses_df = courses_df.merge(department, left_index=True, right_index=True)
courses_df.to_json("./website/data/nodes.json", orient="records")

# Create department.json
departments_df = pd.DataFrame(
    {"department_code": department_codes, "department_name": department_names}
)
departments_df.to_json("./website/data/departments.json", orient="records")