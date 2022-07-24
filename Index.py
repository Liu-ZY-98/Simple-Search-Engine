from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

import re
import json
import os
import math

docID = 0
inverse_index = {}
docID_to_doc = {}


def parse(input):
    s = PorterStemmer()
    inputWordsList = input.split()
    tokenList = []
    # print(inputWordsList)

    for w in inputWordsList:
        tokens = re.sub(r'\\n', ' ', str(w))
        tokens = re.sub(r'\\t', ' ', tokens)
        tokens = re.sub(r'\\r', ' ', tokens)

        tokens = re.sub('[^A-Za-z0-9]+', ' ', tokens)

        tokens = tokens.lower()
        tokens = tokens.strip()

        tokenContent = tokens.split()
        if len(tokenContent) == 1:
            stemmed = s.stem(tokens)
            if len(stemmed) > 1:
                tokenList.append(stemmed)
        elif len(tokenContent) > 1:
            for token in tokenContent:
                stemmed = s.stem(token)
                if len(stemmed) > 1:
                    tokenList.append(stemmed)
    return tokenList


def calcTFIDF():
    for term, doc in inverse_index.items():
        for doc_id, tf in doc.items():
            tfidf = tf * math.log10(docID/len(doc))
            inverse_index[term][doc_id] = float(tfidf)


if __name__ == '__main__':
    for subdir, dirs, files in os.walk('DEV'):
        for filename in files:
            if (filename.startswith('.')):
                continue
            docID += 1
            fileTokens = []
            soup = BeautifulSoup(open(os.path.join(subdir, filename)), 'html.parser')

            # <b> tag: Bold text
            # <p> tag: Paragraph
            # <title> tag: Title
            # <h1>--<h6> tags: Headings
            for content in soup.findAll(['p', 'b', 'title', re.compile('^h[1-6]$')]):
                content = content.get_text().strip()
                # print(content)
                fileTokens += parse(content)
            # content = soup.get_text().strip()
            # print(filename)
            # print(soup.prettify())
            # print(fileTokens)
            for token in fileTokens:
                if token not in inverse_index.keys():
                    tf_dic = {}
                    tf_dic[docID] = 1/len(fileTokens)
                    inverse_index[token] = tf_dic
                else:
                    if docID not in inverse_index[token].keys():
                        inverse_index[token][docID] = 1/len(fileTokens)
                    else:
                        inverse_index[token][docID] += 1/len(fileTokens)
            docID_to_doc[docID] = os.path.join(subdir, filename)[4:].strip()
            print(docID)

            # if docID % 10000 == 0:
            #     calcTFIDF()
            #     index_file = open('test.txt', 'a')
            #     json.dump(inverse_index, index_file)
            #     index_file.close()
            #     docID_file = open('test1.txt', 'a')
            #     json.dump(docID_to_doc, docID_file)
            #     docID_file.close()
            #     inverse_index = {}
            #     docID_to_doc = {}

    calcTFIDF()

    test = open('test.txt', 'w')
    json.dump(inverse_index, test)
    test.close()
    test1 = open('test1.txt', 'w')
    json.dump(docID_to_doc, test1)
    test1.close()

    print('docnum', docID)
    print('uniWord', len(inverse_index))
    #print(inverse_index)