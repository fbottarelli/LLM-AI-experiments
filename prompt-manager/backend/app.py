from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('prompts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    conn = get_db_connection()
    prompts = conn.execute('SELECT * FROM prompts').fetchall()
    conn.close()
    return jsonify([dict(prompt) for prompt in prompts])

@app.route('/api/prompts', methods=['POST'])
def create_prompt():
    new_prompt = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO prompts (content, category) VALUES (?, ?)',
                   (new_prompt['content'], new_prompt['category']))
    conn.commit()
    prompt_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': prompt_id, **new_prompt}), 201

@app.route('/api/prompts/<int:prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    updated_prompt = request.json
    conn = get_db_connection()
    conn.execute('UPDATE prompts SET content = ?, category = ? WHERE id = ?',
                 (updated_prompt['content'], updated_prompt['category'], prompt_id))
    conn.commit()
    conn.close()
    return jsonify(updated_prompt)

@app.route('/api/prompts/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM prompts WHERE id = ?', (prompt_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)