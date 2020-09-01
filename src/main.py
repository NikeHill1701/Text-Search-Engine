import Query
import Indexer
import gui
from tkinter import *

def listen_for_queries():
    while 1:
        query_string = input("Please input your text-query or enter None to exit.\n")
        if query_string == "None":
            break
        query = Query.Query()
        results = query.text_query(query_string)
        count = 1
        for score, file_name in results:
            print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
            count += 1

def answer_phrase_queries(phrase_string):
    query = Query.Query()
    results = query.phrase_query(phrase_string)
    count = 1
    for score, file_name in results:
        print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
        count += 1

def answer_text_queries(query_string):
    query = Query.Query()
    results = query.text_query(query_string)
    count = 1
    for score, file_name in results:
        print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
        count += 1

if __name__ == "__main__":
    print("Aloha!")
    path_to_text_corpus = "/home/nikhil/Desktop/Text-Search-Engine/text_corpus"
    indexer = Indexer.Indexer()
    print("Indexer object created!")
    #ndexer.build_index(path_to_text_corpus)
    print("Index building success!!!")
    #listen_for_queries()
    root = Tk()
    root.geometry("400x300")
    app = gui.Window(root)
    root.mainloop()
