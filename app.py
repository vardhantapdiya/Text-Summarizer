import nltk
from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
nltk.download('punkt')


app = Flask(__name__)

def summarize():
    text = request.form['text']
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    # print(stop_words)
    filtered_words = [word for word in words if word not in stop_words]
    word_frequencies = FreqDist(filtered_words)
    sentence_scores = {}
    
    for sentence in sentences: # Iterating through each sentence in input text
        for word in word_tokenize(sentence.lower()):  #tokenizing each sentence into words and converting them into lower case 
            if word in word_frequencies:  # checking if the word is present in the frequency distribution 
                if len(sentence.split(' ')) < 30:  
                    if sentence not in sentence_scores:   #if the sentences is not present in the sentence_scores dictionary
                        sentence_scores[sentence] = word_frequencies[word]  #Adding the word frequency to the sentence score
                    else: 
                        sentence_scores[sentence] += word_frequencies[word] #Adding the word frequency to the existing sentence scores
    summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    print(summary)
    return summary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def summarize_text():
    summary = summarize()
    text = request.form['text']
    return render_template('summary.html', summary=summary, text=text)

if __name__ == '__main__':
    app.run(debug=False)
