from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# Load CSV data
df = pd.read_csv('airport_reviews.csv')

# Extract text data and combine into a single string
texts = df['content'].astype(str).tolist()
corpus = ' '.join(texts)

# Lowercase the text
corpus = corpus.lower()

# Handle punctuation by adding a space before periods for better tokenization
corpus = corpus.replace('.', ' .')

def build_transition_matrix(text, n):
    words = text.split()
    transition_matrix = {}
    for i in range(len(words) - n):
        prefix = tuple(words[i:i + n])
        suffix = words[i + n]
        if prefix not in transition_matrix:
            transition_matrix[prefix] = []
        transition_matrix[prefix].append(suffix)
    return transition_matrix

def generate_text(transition_matrix, n, length=100):
    current_state = random.choice(list(transition_matrix.keys()))
    result = list(current_state)

    for _ in range(length):
        if current_state in transition_matrix:
            next_state = random.choice(transition_matrix[current_state])
            result.append(next_state)
            current_state = tuple(result[-n:])
        else:
            break

    return ' '.join(result)

# Build transition matrix
transition_matrix = build_transition_matrix(corpus, n=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_text = ""
    if request.method == 'POST':
        length = int(request.form.get('length', 500))
        generated_text = generate_text(transition_matrix, n=2, length=length)
    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
