from Levenshtein import distance

def edit_distance(file1, file2):
    f1 = open(file1)
    text1 = f1.read()
    f1.close()
    
    f2 = open(file2)
    text2 = f2.read()
    f2.close()

    return distance(text1, text2)