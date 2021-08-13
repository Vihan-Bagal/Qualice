# Created by Vihan Bagal
# Date 08/12/2021

from tkinter import *
from tkinter import filedialog
from tkinter import font
import time
import pkg_resources
from symspellpy import SymSpell, Verbosity
start_time = time.time()

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")

bigram_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_bigramdictionary_en_243_342.txt")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)

root = Tk()
root.title("Qualice")
root.geometry("700x515")
root.iconbitmap('file:///Users/vihanbagal/009c956c949590749fdddf7b06e0e273_Mos.icns')
isInsert = True
TextMode = True
checkCounter = 0
prevWords = ""


main_frame = Frame(root)
main_frame.pack(pady=5, fill=BOTH, expand=1)

text_scroll = Scrollbar(main_frame)
text_scroll.pack(side=RIGHT, fill=Y)


text_box = Text(main_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="#009999", selectforeground="#D8DFE9", undo=True, yscrollcommand=text_scroll.set, background="#353446", fg="#D8DFE9", padx=7, insertbackground="#D8DFE9", insertofftime=0)
text_box.pack(fill=BOTH, expand=1)
text_scroll.config(command=text_box.yview)

def new_file(event):
    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    root.title("Unnamed File")
    text_box.config(state=DISABLED)

def insert(event):
    global isInsert
    isInsert = True

def escape_insert(event):
    global isInsert
    isInsert = False

def retrieve_input():
    input = text_box.get("1.0",END)
    return input.split()
def open_file(event):
    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="/Users/vihanbagal", title="Open File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"), ("Python Files", "*.py"), ("HTML Files", "*.html")))
    name = text_file
    name = name.replace("/Users/vihanbagal", "")

    text_file = open(text_file, 'r')
    stuff = text_file.read()

    text_box.insert(END, stuff)
    text_file.close()
    text_box.config(state=DISABLED)
def enter_Text_mode(event):
    global TextMode
    TextMode = True

def exit_Text_mode(event):
    global TextMode
    TextMode = False

def delete_Line(event):
    text_box.delete()

def SaveAs_File(event):
    text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"), ("Python Files", "*.py"), ("HTML Files", "*.html")))
    if text_file:
        name = text_file
        name = name.replace("/Users/vihanbagal", "")

        text_file = open(text_file, 'w')
        text_file.write(text_box.get(1.0, END))

        text_file.close()


def Spell_Check():
    global prevWords
    counter = 0
    words = retrieve_input()
    wordstring = ' '.join(words)
    if (words == "" or words == prevWords):
        return
    suggestions = sym_spell.lookup_compound(wordstring, max_edit_distance=2,
                                        transfer_casing=True)
    for suggestion in suggestions:
        wordlist = (suggestion.term).split()
        for w in words:
            if(counter < len(wordlist)):
                if(w != wordlist[counter]):
                    searchWord(w, True)
                if(w == wordlist[counter]):
                    searchWord(w, False)
            else:
                return
            counter = counter+1

    
def searchWord(word, errorize):
    text_box.tag_config("red_tag", foreground="red", underline=1)
    offset = '+%dc' % len(word)

    pos_start = text_box.search(word, '1.0', END)

    while pos_start:

        # create end position by adding (as string "+5c") number of chars in searched word 
        pos_end = pos_start + offset

        # add tag
        if(errorize):
            text_box.tag_add('red_tag', pos_start, pos_end)
        if(errorize == False):
            text_box.tag_remove('red_tag', pos_start, pos_end)

        # search again from pos_end to the end of text (END)
        pos_start = text_box.search(word, pos_end, END)


root.bind("<Escape>", escape_insert)
def main():
    global checkCounter
    if(isInsert == False):
        text_box.config(state=DISABLED)
        root.bind("<n>", new_file)
        root.bind("<i>", insert)
        root.bind("<o>", open_file)
        root.bind("<t>", enter_Text_mode)
        root.bind("<T>", exit_Text_mode)
        root.bind("<S>", SaveAs_File)

    if(isInsert == True):
        text_box.config(state=NORMAL)
        root.unbind("<n>")
        root.unbind("<i>")
        root.unbind("<o>")
        root.unbind("<t>")
        root.unbind("<T>")
        root.unbind("<S>")
    if(TextMode):
        if((((time.time()-start_time) - (checkCounter * 0.5)) > 0.5)):
            Spell_Check()
            checkCounter = checkCounter+1
        
    



status_bar = Label(root, text="Insert      ", anchor=E, fg="#D8DFE9")
status_bar.pack(fill=X, side=BOTTOM, ipady=5)


while True:
    main()
    root.update_idletasks()
    root.update()
