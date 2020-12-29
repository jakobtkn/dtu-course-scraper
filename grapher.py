import pickle
from course import Course

with open('course_dictionary.pickle', 'rb') as handle:
    courseDict = pickle.load(handle)

print(courseDict["01018"].rec_reqs)
