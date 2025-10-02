#!/usr/bin/env python

import spacy
import sys
import json

nlp = spacy.load("/var/ner_app/model")
param1 = sys.argv[1].strip()
doc_result = nlp(param1)

bio_results=[]

for entity in doc_result.ents:
    if entity.label_=='O':
        bio_results.append({'start_index': entity.start_char, 'end_index': entity.end_char, 'entity': entity.label_})
    else:
        entity_words = entity.text.split()
        bio_result = []
        start_char = entity.start_char
        end_char = entity.end_char

        for word in entity_words:
            if not bio_result:
                label = "B-" + entity.label_
            else:
                label = "I-" + entity.label_
            end_char = start_char + len(word)
            bio_result.append({'start_index': start_char, 'end_index': end_char, 'entity': label})
            start_char = start_char+end_char+1

        for result in bio_result:
            bio_results.append(result)

print(json.dumps(bio_results, indent=0))