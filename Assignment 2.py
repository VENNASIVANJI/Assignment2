from bs4 import BeautifulSoup

def extract_text_from_html(html_file):
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()
import PyPDF2

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
pip install elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch()

def index_document(doc_id, content):
    es.index(index="cdp_docs", id=doc_id, body={"content": content})

content = extract_text_from_html('document.html')
index_document(1, content)
pip install flask spacy elasticsearch
python -m spacy download en_core_web_sm
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import spacy

app = Flask(__name__)
es = Elasticsearch()

nlp = spacy.load("en_core_web_sm")

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('query')
    
    doc = nlp(user_input)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]

    search_results = es.search(index="cdp_docs", body={
        "query": {
            "multi_match": {
                "query": ' '.join(keywords),
                "fields": ["content"]
            }
        }
    })

    hits = search_results['hits']['hits']
    if hits:
        response = hits[0]['_source']['content']
    else:
        response = "Sorry, I couldn't find relevant information."

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
npx create-react-app cdp-chatbot
cd cdp-chatbot
npm install bootstrap axios
import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!message) return;

    setConversation([...conversation, { sender: 'user', text: message }]);
    setMessage('');
    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/ask', { query: message });
      setConversation([...conversation, { sender: 'user', text: message }, { sender: 'bot', text: response.data.response }]);
    } catch (error) {
      setConversation([...conversation, { sender: 'user', text: message }, { sender: 'bot', text: 'Error occurred. Please try again.' }]);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h3>CDP Support Chatbot</h3>
      <div className="chat-box">
        {conversation.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          className="form-control"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask a question"
        />
        <button onClick={handleSendMessage} className="btn btn-primary mt-2">
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};
pip install faiss-cpu
import faiss
import numpy as np

vectors = np.array([nlp(text).vector for text in documents])
index = faiss.IndexFlatL2(vectors.shape[1])  
index.add(vectors)  

query_vector = nlp('Segment vs Lytics').vector
D, I = index.search(np.array([query_vector]), k=5)
# CDP Support Chatbot

## Overview

This is a chatbot built for providing support and answering questions related to various Customer Data Platforms (CDPs). The chatbot is powered by natural language processing (NLP) using spaCy and indexes CDP documentation using Elasticsearch.

## Tech Stack
- **Frontend**: React.js, Bootstrap
- **Backend**: Python (Flask)
- **NLP/Indexer**: spaCy, Elasticsearch
- **Hosting**: AWS/Heroku

## Features
- Ask questions about various CDPs (e.g., Segment, Lytics)
- Retrieve relevant answers from indexed documentation
- Multi-CDP comparison
- Advanced configurations and integrations guide

## Setup

### Backend Setup:
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install flask spacy elasticsearch
   python -m spacy download en_core_web_sm

npm install
npm start
