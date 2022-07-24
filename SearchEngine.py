import json
import re
from nltk.stem import PorterStemmer

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

def search_word(word):
    doc_sort = sorted(inverse_index[word].items(), key = lambda x: x[1], reverse = True)
    doc_sort = doc_sort[:1000]
    return doc_sort

if __name__ == '__main__':
    print('Loading Index...')
    index_file = open('test.txt', 'r')
    docID_file = open('test1.txt', 'r')
    inverse_index = json.loads(index_file.read())
    docID_to_doc = json.loads(docID_file.read())
    index_file.close()
    docID_file.close()


    print('Load complete, you can use now. ')
    while True:
        search_input = input('enter search queries or enter "Quit" to quit: ')
        search_input = (search_input.lower()).strip()

        search_terms = {}
        term_dict = {}

        if search_input == 'quit':
            print('Thank you for using the search engine, have a nice day!')
            break
        else:
            search_input = parse(search_input)
            print(search_input)
            for word in search_input:
                search_terms[word] = search_word(word)
            for docs in search_terms.values():
                for doc in docs:
                    if doc[0] in term_dict:
                        term_dict[doc[0]] += float(doc[1])
                    else:
                        term_dict[doc[0]] = float(doc[1])
            # print(search_terms)
            term_dict = sorted(term_dict.items(), key = lambda x: x[1], reverse = True)
            print(term_dict)
            result = []
            for page in term_dict:
                result.append(page[0])
            result = result[:25]

            if len(page) == 0:
                print('Search for this is not possible.')
            else:
                print('THE TOP 25 RESULTS ARE:  ')
                for x in result:
                    print(docID_to_doc[x])
