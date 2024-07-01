

from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

app = Flask(__name__)

# Load the model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize FAISS index
index = faiss.IndexFlatL2(384)  # Dimension should match the model output

# Dictionary to store post embeddings
post_embeddings = {}

@app.route('/update_embeddings', methods=['POST'])
def update_embeddings():
    data = request.get_json()
    post_id = data['ID']
    text = data['content']
    embedding = model.encode(text)
    embedding = np.array([embedding]).astype('float32')

    # Store in FAISS index
    index.add(embedding)
    post_embeddings[post_id] = embedding

    return jsonify({'status': 'success', 'post_id': post_id})

@app.route('/get_post_embedding/<int:post_id>', methods=['GET'])
def get_post_embedding(post_id):
    embedding = post_embeddings.get(post_id)
    if embedding is not None:
        return jsonify(embedding.tolist())
    else:
        return jsonify({'status': 'error', 'message': 'Post not found'})

@app.route('/search', methods=['POST'])
def search():
    query = request.get_json()['query']
    query_embedding = model.encode(query)
    query_embedding = np.array([query_embedding]).astype('float32')
    
    D, I = index.search(query_embedding, 5)
    results = [list(post_embeddings.keys())[i] for i in I[0]]

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
