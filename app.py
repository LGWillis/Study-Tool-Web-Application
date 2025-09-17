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
                .arrow {
                    font-size: 2em;
                    cursor: pointer;
                    user-select: none;
                    margin: 0 20px;
                }
                .controls {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        </head>
        <body>
            <h1>Flashcards</h1>
            <a href="{{ url_for('add_flashcard') }}">Add Flashcard</a>
            {% if flashcards %}
                <div class="controls">
                    <span class="arrow" id="left-arrow">&#8592;</span>
                    <div class="flashcard" id="flashcard" onclick="revealAnswer()">
                        <div class="question" id="question"></div>
                        <div class="answer" id="answer" style="display:none;"></div>
                    </div>
                    <span class="arrow" id="right-arrow">&#8594;</span>
                </div>
                <script>
                    const flashcards = {{ flashcards|tojson }};
                    let current = 0;
                    function showCard(idx) {
                        document.getElementById('flashcard').classList.remove('revealed');
                        document.getElementById('question').style.display = 'block';
                        document.getElementById('answer').style.display = 'none';
                        document.getElementById('question').textContent = flashcards[idx].question;
                        document.getElementById('answer').textContent = flashcards[idx].answer;
                    }
                    function revealAnswer() {
                        document.getElementById('question').style.display = 'none';
                        document.getElementById('answer').style.display = 'block';
                    }
                    document.getElementById('left-arrow').onclick = function() {
                        if (current > 0) current--;
                        else current = flashcards.length - 1;
                        showCard(current);
                    };
                    document.getElementById('right-arrow').onclick = function() {
                        if (current < flashcards.length - 1) current++;
                        else current = 0;
                        showCard(current);
                    };
                    showCard(current);
                </script>
            {% else %}
                <p>No flashcards yet.</p>
            {% endif %}
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
