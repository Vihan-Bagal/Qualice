from nltk import *

f = open("NLP-Data.txt", "r")
article = f.read()

split_article = tokenize.sent_tokenize(article)

