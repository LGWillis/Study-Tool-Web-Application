from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# In-memory storage for flashcards
flashcards = []


# Home page: list all flashcards
@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head>
            <title>Flashcards</title>
            <style>
                .flashcard {
                    width: 300px;
                    height: 150px;
                    margin: 20px auto;
                    background: #f8f8f8;
                    border: 2px solid #333;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.2em;
                    cursor: pointer;
                    transition: box-shadow 0.2s;
                    box-shadow: 2px 2px 8px #aaa;
                    position: relative;
                }
                .flashcard .answer {
                    display: none;
                }
                .flashcard.revealed .question {
                    display: none;
                }
                .flashcard.revealed .answer {
                    display: block;
                }
            </style>
        </head>
        <body>
            <h1>Flashcards</h1>
            <a href="{{ url_for('add_flashcard') }}">Add Flashcard</a>
            {% if flashcards %}
                {% for card in flashcards %}
                    <div class="flashcard" onclick="this.classList.toggle('revealed')">
                        <div class="question">{{ card['question'] }}</div>
                        <div class="answer">{{ card['answer'] }}</div>
                    </div>
                {% endfor %}
            {% else %}
                <p>No flashcards yet.</p>
            {% endif %}
            <script>
                // No extra JS needed, handled by onclick toggle
            </script>
        </body>
        </html>
    ''', flashcards=flashcards)

# Add flashcard page
@app.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        if question and answer:
            flashcards.append({'question': question, 'answer': answer})
            return redirect(url_for('index'))
    return render_template_string('''
        <h1>Add Flashcard</h1>
        <form method="post">
            <label>Question:</label><br>
            <input type="text" name="question" required><br>
            <label>Answer:</label><br>
            <input type="text" name="answer" required><br><br>
            <input type="submit" value="Add">
        </form>
        <a href="{{ url_for('index') }}">Back to Flashcards</a>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
