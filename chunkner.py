import pickle
import nltk
from nltk.tag import SennaChunkTagger
from nltk.tag import StanfordNERTagger

filep = open('out', 'rb')
mydict = pickle.load(filep)
filep.close()

lines = []
filet = open('input', 'r')
for line in filet:
    lines.append(nltk.word_tokenize(line))


chunks = []
tagger = SennaChunkTagger('/home/senna')
for line in lines:
    chunks.append(tagger.tag(line))


flatchunks = [val for sublist in chunks for val in sublist]

entities = []
st = StanfordNERTagger('/home/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz', '/home/stanford-ner/stanford-ner.jar', encoding='utf-8')
for line in lines:
    entities.append(st.tag(line))


flatentities = [val for sublist in entities for val in sublist]

chunknerdict = []
filet.close()
delta = 0
for index, value in enumerate(mydict):
    print(index, value)
    chunk = flatchunks[index-delta]
    entity = flatentities[index-delta]
    print(value[0], chunk[0])
    if value[0] == chunk[0]:
        chunknerdict.append((value[0], chunk[1], entity[1], value[1]))
    else:
        delta = 1


print(chunknerdict)

with open('out_to_process', 'wb') as fp:
    pickle.dump(chunknerdict, fp)
fp.close()
