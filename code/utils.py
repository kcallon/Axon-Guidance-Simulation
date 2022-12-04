from Levenshtein import *

def edit_distance(file1, file2):
    text1 = open(file1).read()
    text2 = open(file2).read()

    return distance(text1, text2)