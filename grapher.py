import pickle
from course import Course

with open('course_dictionary.pickle', 'rb') as handle:
    courseDict = pickle.load(handle)

for course in courseDict.values():
    print(course.id)
    print(course.obl_reqs)
    print(course.rec_reqs)
    print(course.blocks)
    print()