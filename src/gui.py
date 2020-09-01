from tkinter import *
import main
import Indexer
import Query

class Window(Frame):

    text_query_entry = None
    phrase_query_entry = None
    results_entry = None
    #results_text = StringVar()

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        Frame.__init__(self, master)
        self.init_window()
        self.master = master

    def init_window(self):

        self.master.title("Text-Search-Engine")
        self.pack(fill=BOTH, expand=1)

        text_query_label = Label(self, text="Text Query")
        self.text_query_entry = Entry(self)

        text_query_label.grid(row=0, column=1)
        self.text_query_entry.grid(row=0, column=2)

        phrase_query_label = Label(self, text="Phrase Query")
        self.phrase_query_entry = Entry(self)

        phrase_query_label.grid(row=1, column=1)
        self.phrase_query_entry.grid(row=1, column=2)
    
        results_label = Label(self, text="Results")
        self.results_entry = Text(self, height=20, width=100)

        results_label.grid(row=2, column=1)
        self.results_entry.grid(row=2, column=2)

        search_button = Button(self, text="Search", command=self.answer_text_queries)
        search_button.grid(row=3, column=2)

        quit_button = Button(self, text="Quit", command=self.client_exit)
        quit_button.grid(row=3, column=3)

    def answer_phrase_queries(self):
        phrase_string = self.phrase_query_entry.get()
        query = Query.Query()
        results = query.phrase_query(phrase_string)
        count = 1
        for score, file_name in results:
            print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
            count += 1

    def answer_text_queries(self):
        query_string = self.text_query_entry.get()
        query = Query.Query()
        print("Query instance successfully creater!")
        results = query.text_query(query_string)
        print("Results obtained!!")
        results = list(results)
        self.print_results(results)
        """count = 1
        for score, file_name in results:
            print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
            count += 1
        """

    def print_results(self, results):
        results_string = ""
        count = 1
        for score, file_name in results:
            results_string += "Choice number: " + str(count) + " --> File: " + file_name + " Score = " + str(score) + "\n";
            count += 1
        results_string += "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        #self.results_entry.delete(0, END)
        self.results_entry.insert(INSERT, results_string)
        #self.results_text.set(results_string)

    def client_exit(self):
        exit()

