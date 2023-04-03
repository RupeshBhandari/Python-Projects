import pandas as pd

students = {
    'SN': [1,2,3],
    'Name': ['Ram', 'Syam', 'fas']
}

course = {
    'Course ID': [111, 222, 333],
    'Course Name': ['Python', 'Java', 'C++']
}

students_df = pd.DataFrame(students)
course_df = pd.DataFrame(course)

print(students_df)
print(course_df)

print(students_df + course_df)
# print(df['first_column'].to_list())
# print(df.describe())
# print(df.iloc[:,:])