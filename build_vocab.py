import numpy as np
from tensorflow.contrib import learn
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

x_text = list()
with open(sys.argv[1]) as f:
    for line in f:
        x_text.append(unicode(line[:-1]))

vocabulary = set()

lang = sys.argv[1].split('.')[-1].lower()
print lang

if lang == "sparql":
    
    for x in x_text:
        for t in x.split(" "):
            vocabulary.add(t)

else: # any other language

    # x_text = ['This is a cat','This must be boy', 'This is a a dog']
    max_document_length = max([len(x.split(" ")) for x in x_text])

    ## Create the vocabularyprocessor object, setting the max lengh of the documents.
    vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)

    ## Transform the documents using the vocabulary.
    x = np.array(list(vocab_processor.fit_transform(x_text)))    

    ## Extract word:id mapping from the object.
    vocab_dict = vocab_processor.vocabulary_._mapping

    ## Sort the vocabulary dictionary on the basis of values(id).
    ## Both statements perform same task.
    #sorted_vocab = sorted(vocab_dict.items(), key=operator.itemgetter(1))
    sorted_vocab = sorted(vocab_dict.items(), key = lambda x : x[1])

    ## Treat the id's as index into list and create a list of words in the ascending order of id's
    ## word with id i goes at index i of the list.
    vocabulary = set(list(zip(*sorted_vocab))[0])
    
    to_remove = set()
    to_add = set()
    for t0 in vocabulary:
        if "'" in t0:
            to_remove.add(t0)
            for t1 in t0.split("'"):
                to_add.add(t1)
    for t0 in to_remove:
        vocabulary.remove(t0)
    for t0 in to_add:
        vocabulary.add(t0)
    
# print(vocabulary)
# print(x)
for v in vocabulary:
    if v != "":
        print v
