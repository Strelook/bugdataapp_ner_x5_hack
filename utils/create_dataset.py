import pandas as pd
import spacy
from spacy.tokens import DocBin
#from collections import defaultdict
#import math
#import random
import ast
import re

nlp = spacy.blank("ru")

def to_spacy(data, nlp):
    doc_bin = DocBin()
    for item in data.itertuples():
        doc = nlp.make_doc(item.sample)
        ents = []

        eval_annotations = ast.literal_eval(item.annotation)
        print(eval_annotations)

        imploded_annotations = []
        current_annotation = []
        for annotation in eval_annotations:
            if re.search(r"I-.*", annotation[2]):
                current_annotation[1] = annotation[1]
                current_annotation[2] = annotation[2]
            else:
                if current_annotation:
                    imploded_annotations.append(tuple(current_annotation))
                current_annotation = list(annotation)
            
        if current_annotation:
            imploded_annotations.append(tuple(current_annotation))
            current_annotation = []

        for start, end, label in imploded_annotations:

            if re.search(r"B-.*|I-.*", label):
                label = label[2:]

            print([start, end, label])
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
            print(span)
        doc.ents = ents
        if doc:
            doc_bin.add(doc)
    return doc_bin

train_data_csv = pd.read_csv('train_CUT.csv', delimiter=';')

# Конвертируем данные в формат spacy и сохраняем
train_doc_bin = to_spacy(train_data_csv, nlp)
train_doc_bin.to_disk("train.spacy")

input("Press Enter to continue...")