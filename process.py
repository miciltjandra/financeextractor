import os.path
import pickle
import random
import json
from collections import Counter
import sklearn_crfsuite
from sklearn_crfsuite import metrics

print('Loading data...')

mydict = []
names = os.listdir('.')
random.shuffle(names)
for i, name in enumerate(names):
    if name[:6] == 'out_cn':
        file = open(name, 'rb')
        mydict.append(pickle.load(file))
        file.close()
    elif name[:6] == 'out_to':
        file = open(name, 'rb')
        to_append = pickle.load(file)
        file.close()

mydict.append(to_append)

text = []
feature = []
label = []
for art in mydict:
    articles = []
    for obj in art:
        articles.append(obj[0])
    text.append(articles)


def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    nertag = sent[i][2]
    features = {
        'bias': 1.0,
        'lower': word.lower(),
        'suffix3': word[-3:],
        'suffix2': word[-2:],
        'preffix3': word[:3],
        'preffix2': word[:2],
        'isupper': word.isupper(),
        'istitle': word.istitle(),
        'isdigit': word.isdigit(),
        'postag': postag,
        'nertag': nertag
    }
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        nertag1 = sent[i - 1][2]
        features.update({
            '-lower': word1.lower(),
            '-istitle': word1.istitle(),
            '-isupper': word1.isupper(),
            '-postag': postag1,
            '-nertag': nertag1
        })
    else:
        features['BOS'] = True
    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        nertag1 = sent[i + 1][2]
        features.update({
            '+lower': word1.lower(),
            '+istitle': word1.istitle(),
            '+isupper': word1.isupper(),
            '+postag': postag1,
            '+nertag': nertag1
        })
    else:
        features['EOS'] = True
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [lbel for token, ptag, ner, lbel in sent]


print('Creating training & testing data...')
X_train = [sent2features(s) for s in mydict[:-1]]
y_train = [sent2labels(s) for s in mydict[:-1]]
X_test = [sent2features(s) for s in mydict[-1:]]

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1='0.1',
    c2='0.1',
    max_iterations=100,
    all_possible_transitions=True,
    verbose=True
)

crf.fit(X_train, y_train)
print('Hooray you have trained the model')

y_pred = crf.predict(X_test)

arr = []

for ida, art in enumerate(X_test):
    for idx, item in enumerate(art):
        arr.append((item['lower'], y_pred[ida][idx]))

# Extract from BIO tag
who = []
why = []
howmuch = []
when = []
for tuple in arr:
    if tuple[1] == "B-who":
        who.append(tuple[0])
    elif tuple[1] == "I-who":
        who[len(who) - 1] += " "
        who[len(who) - 1] += tuple[0]
    elif tuple[1] == "B-why":
        why.append(tuple[0])
    elif tuple[1] == "I-why":
        why[len(why) - 1] += " "
        why[len(why) - 1] += tuple[0]
    elif tuple[1] == "B-when":
        when.append(tuple[0])
    elif tuple[1] == "I-when":
        when[len(when) - 1] += " "
        when[len(when) - 1] += tuple[0]
    elif tuple[1] == "B-howmuch":
        howmuch.append(tuple[0])
    elif tuple[1] == "I-howmuch":
        howmuch[len(howmuch) - 1] += " "
        howmuch[len(howmuch) - 1] += tuple[0]

# print(bestwho)
print('Who')
print(who)
print('When')
print(when)
print('How much')
print(howmuch)
print('Why')
print(why)

jsonobj = {'who': who, 'when': when, 'howmuch': howmuch, 'why': why}
with open('out.json', 'w') as f:
    json.dump(jsonobj, f)

def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))


print("Top likely transitions:")
print_transitions(Counter(crf.transition_features_).most_common(10))

print("\nTop unlikely transitions:")
print_transitions(Counter(crf.transition_features_).most_common()[-10:])


def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-8s %s" % (weight, label, attr))


print("Top positive:")
print_state_features(Counter(crf.state_features_).most_common(15))

print("\nTop negative:")
print_state_features(Counter(crf.state_features_).most_common()[-15:])
