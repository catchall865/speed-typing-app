from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

global WORDS_DF
WORDS_DF = pd.read_csv(resource_path('assets\\words.csv'))

FONT = 'LATO'

class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        
        self.configure(bg='#9376E0')
        self.title('Test Your Typing Speed')

        self.frm = Frame(self, bg='#9376E0')
        self.frm.grid(padx=15, pady=15)

        self.bg_img = Image.open(resource_path('assets\\sticky-note.png'))
        self.bg_img = self.bg_img.resize((800, 800))

        self.bg_img_pi = ImageTk.PhotoImage(self.bg_img)
        self.bg_panel = Label(self.frm, image=self.bg_img_pi, bg='#9376E0')
        self.bg_panel.grid(row=1, column=1)

        # set and reset word lists and labels
        key_words_list = []
        user_words_list =[]
        label_list = []

        self.words_list = [WORDS_DF.sample().iloc[0].sample().iloc[0] for i in range(5)]

        def show_words():
            for i in range(len(self.words_list)):
                label_var = StringVar()
                label_var.set(self.words_list[i])
                self.word_label = Label(self.frm, textvariable=label_var, font=(FONT, 45), bg='#E893CF')
                self.word_label.place(relx=0.35, rely=0.27+(i+1)*0.0723)
                label_list.append(self.word_label)

        def add_entry_to_list():
            text = self.user_entry.get()
            mini_word_list = text.split(' ')
            for word in mini_word_list:
                user_words_list.append(word)
            self.user_entry.delete(0, END)

        def update_labels(event):
            add_entry_to_list()
            for word in self.words_list:
                key_words_list.append(word)
            self.words_list = [WORDS_DF.sample().iloc[0].sample().iloc[0] for i in range(5)]
            for i in range(len(self.words_list)):
                label_var = StringVar()
                label_var.set(self.words_list[i])
                label_list[i].config(textvariable=label_var)

        self.user_entry = Entry(self.frm, width=50)
        self.user_entry.grid(column=1, row=2, pady=15)
        self.user_entry.configure(font=(FONT, 20))
        self.user_entry.focus_set()
        self.user_entry.bind('<Return>', update_labels)

        def compare_lists(user_list, key_list):
            number_correct = 0
            for word in user_list:
                if word in key_list:
                    number_correct += 1
            try:
                percent_correct = (number_correct/len(key_list))*100
            except ZeroDivisionError:
                percent_correct = 0.0
            self.score_label = Label(self.frm, text=f'You typed {len(user_list)} words per minute\n with {percent_correct}% accuracy', font=(FONT, 35), bg='#E893CF')
            self.score_label.grid(column=1, row=1)

            self.user_entry.destroy()

        self.countdown_label = Label(self.frm, bg='#9376E0', font=(FONT, 60), fg='white')
        self.countdown_label.grid(row=0, column=1, pady=10)

        def countdown(count):
            self.countdown_label['text'] = count
            if count > 0:
                self.after(1000, countdown, count-1)
            else:
                for label in label_list:
                    label.destroy()
                compare_lists(user_words_list, key_words_list)

        def start_game():
            self.start_button.destroy()
            self.instructions.destroy()
            show_words()
            countdown(60)

        self.start_button = Button(self.frm, text='Click here to start!', command=start_game, font=(FONT, 30))
        self.start_button.grid(column=1, row=0)

        instructions_text = 'You have 60 seconds to type as many words as you can.\nYou will be served 5 words at a time.\nType out each word with a space between.\nPress Enter when you finish the last word.\nType carefully! You will not be told if you misspelled a word!'

        self.instructions = Label(self.frm, text=instructions_text, justify='left', font=(FONT, 20))
        self.instructions.place(relx=.5, rely=.5, anchor='center')


if __name__ == '__main__':
    gui = App()
    gui.mainloop()