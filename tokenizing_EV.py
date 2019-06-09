import pandas as pd
import numpy as np

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
titles = []
contents = []

raw_data = pd.read_excel('raw_data.xlsx', 'sheet1')
raw_titles = raw_data['title']
raw_contents = raw_data['contents']

## make title, contents list of scraped datas
for i in range(len(raw_data)):
	titles.append(raw_titles[i])
	contents.append(raw_contents[i])

#tokenize
docs = [] #store all the tokens of titles and contents

for i in range(0, len(raw_data)):
	title = titles[i]
	content = contents[i]
	title_tokens = word_tokenize(title)
	docs.extend(title_tokens)

	sentences = sent_tokenize(content)
	for sentence in sentences:
		content_tokens = word_tokenize(sentence)
		docs.extend(content_tokens)
'''
for i in range(0, len(raw_data)):
	titles.append(kkma.nouns(uraw_titles[i]))
'''
nltk_text = nltk.Text(docs)
freq_dist = nltk_text.vocab()
print(freq_dist['활성화'])

