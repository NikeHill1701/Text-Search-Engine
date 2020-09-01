import re
import os
import math
import json

class Indexer:
    # The indexer class

    debug = False

    def stem_words(self, word_list):
        """
            TODO: Implement stemming using nltk library
        """
        return word_list


    def process_files(self, directory_path):
        """
            A function to convert all the files in to word-vectors
            This function works only on .txt files for now
            TODO: Write code to process .pdf files too
        """
        # read stopwords from stopwords.txt
        path_to_stopwords = "/home/nikhil/Desktop/Text-Search-Engine/stopwords.txt"

        stopwords = open(path_to_stopwords, 'r').read().lower()
        stopwords = stopwords.split()

        file_to_words = {}
        for file in os.listdir(directory_path):
            if self.debug:
                # print names of the files in the given directory 
                # for debugging purposes
                print(file)
            file_path = os.path.join(directory_path,file)
            pattern = re.compile('[\W_]+')
            words_in_file = open(file_path, 'r').read().lower()
            words_in_file = pattern.sub(' ', words_in_file)
            re.sub(r'[\W_]+', '', words_in_file)
            words_in_file = words_in_file.split()
            words_in_file = self.stem_words(words_in_file)

            # filter out all the stopwords
            file_to_words[file] = [word for word in words_in_file if word not in stopwords]

        #print(file_to_words['test.txt'])

        return file_to_words

    def index_one_file(self,word_list):
        """
            Returns the list of indices where it occours in a file for each word
            Input: word_list of a file
            Output: {word1: [pos1, pos2, ...], word2:[pos1, ..]}
        """
        file_index = {}
        
        for position in range(0,len(word_list)):
            word = word_list[position]
            if word in file_index.keys():
                file_index[word].append(position)
            else:
                file_index[word] = [position]
        return file_index


    def index_all_files(self, word_lists):
        """
            input: {file1:[word1, word2, ..], file2:[word1, word2, ..] }
            output: {file1:{word1:[pos1, ..]. word2:[pos1, ..]}, file2:{word1:[pos1, ..]. word2:[pos1, ..]}}
        """
        index_all = {}
        for file in word_lists.keys():
            index_all[file] = self.index_one_file(word_lists[file])

        return index_all

    def get_inverted_index(self, index):
        inverted_index = {}

        for file in index.keys():
            for word in index[file].keys():
                if word in inverted_index.keys():
                    inverted_index[word][file] = index[file][word]
                else:
                    inverted_index[word] = {file: index[file][word]}

        return inverted_index

    def build_index(self, text_corpus): 
        word_lists = self.process_files(text_corpus)
        index = self.index_all_files(word_lists)
        inverted_index = self.get_inverted_index(index)

        self.build_tf_idf_vectors(inverted_index)
        #print(inverted_index)

        with open("/home/nikhil/Desktop/Text-Search-Engine/index.json", 'w') as indexDB:
            json.dump(inverted_index, indexDB, indent=4)
    
    def build_tf_idf_vectors(self, inverted_index):

        number_of_unique_words = len(inverted_index)
        unique_words = {}

        tf_vector = {}
        idf_vector = [0] * number_of_unique_words
        word_vector = []
        cnt = 0
        for word in inverted_index.keys():
            unique_words[word] = cnt
            word_vector.append(word)
            for file in inverted_index[word].keys():
                if file not in tf_vector.keys():
                    tf_vector[file] = [0] * number_of_unique_words
                tf_vector[file][cnt] += len(inverted_index[word][file])
                if tf_vector[file][cnt] > 0:
                    idf_vector[cnt] += 1
            cnt += 1

        number_of_files = len(tf_vector)
        for i in range(len(idf_vector)):
            idf_vector[i] = math.log(number_of_files / idf_vector[i])

        tf_idf_vector = {}

        for file in tf_vector.keys():
            tf_idf_vector[file] = [x * y for x, y in zip (tf_vector[file], idf_vector)]

        # TODO: dump this tf_idf_vector into a .json file
        with open("/home/nikhil/Desktop/Text-Search-Engine/tf_idf_vector.json", 'w') as tf_idf_json:
            json.dump(tf_idf_vector, tf_idf_json, indent=4)
        # TODO: dump unique_words vector into a .json file
        with open("/home/nikhil/Desktop/Text-Search-Engine/unique_words.json", 'w') as unique_words_json:
            json.dump(unique_words, unique_words_json, indent=4)
        
        if self.debug:
            print(word_vector)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(tf_vector)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(idf_vector)

"""
text_corpus = "/home/nikhil/Desktop/Text-Search-Engine/text_corpus"

indexer = Indexer()
indexer.build_index(text_corpus)
"""


