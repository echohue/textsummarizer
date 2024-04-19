import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from transformers import T5ForConditionalGeneration, T5Tokenizer




def extractsummarizer(rawtext):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawtext)
    #for individual words
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text]+=1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    #for sentence
    sent_tokens = [sent for sent in doc.sents]
    sent_freq = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_freq.keys():
                    sent_freq[sent]=word_freq[word.text]
                else:
                    sent_freq[sent]+=word_freq[word.text]

    select_len = int(len(sent_tokens)*0.3)
    summary = nlargest(select_len,sent_freq,key = sent_freq.get)
    f_summary = [word.text for word in summary]
    summary = ' '.join(f_summary)
    return summary,doc,len(rawtext.split(' ')),len(summary.split(' '))
    
#abstractive summarizer




def abstractsummarizer(document):
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    inputs = tokenizer.encode("summarize: " + document, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary,document
   
