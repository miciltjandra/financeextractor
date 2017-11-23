import nltk

# READ FILES
array = []
file = open('in', 'r')
for line in file:
    print(line)
    inputs = nltk.word_tokenize(line)
    if inputs:
        i = 0
        for word in inputs:
            tup = (word, "O")
            array.append(tup)
            i += 1
print(array)
import pickle

with open('out', 'wb') as fp:
    pickle.dump(array, fp)
file.close()
