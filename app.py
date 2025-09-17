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
                body {
                    background: #181a20;
                    color: #e0e0e0;
                    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                    margin: 0;
                    min-height: 100vh;
                }
                h1 {
                    text-align: center;
                    font-weight: 600;
                    margin-top: 40px;
                    color: #fff;
                }
                a {
                    display: block;
                    text-align: center;
                    margin-bottom: 30px;
                    color: #00bfae;
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.2s;
                }
                a:hover {
                    color: #00e6cf;
                }
                .controls {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 20px;
                }
                .arrow {
                    font-size: 2.5em;
                    cursor: pointer;
                    user-select: none;
                    margin: 0 30px;
                    color: #00bfae;
                    transition: color 0.2s, transform 0.2s;
                }
                .arrow:hover {
                    color: #00e6cf;
                    transform: scale(1.2);
                }
                .flashcard {
                    width: 350px;
                    height: 180px;
                    background: linear-gradient(135deg, #23272f 60%, #222 100%);
                    border: none;
                    border-radius: 16px;
                    box-shadow: 0 4px 24px #000a;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25em;
                    cursor: pointer;
                    position: relative;
                    margin: 0 10px;
                    transition: box-shadow 0.2s, background 0.2s;
                }
                .flashcard:hover {
                    box-shadow: 0 8px 32px #00bfae44;
                    background: linear-gradient(135deg, #23272f 60%, #222 100%);
                }
                .question, .answer {
                    padding: 20px;
                    text-align: center;
                    width: 100%;
                    font-size: 1.15em;
                }
                .answer {
                    color: #00e6cf;
                    font-weight: 500;
                }
                .footer {
                    text-align: center;
                    color: #888;
                    margin-top: 40px;
                    font-size: 0.95em;
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
                <div class="footer">Click the card to reveal the answer. Use arrows to switch cards.</div>
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
                <p style="text-align:center;">No flashcards yet.</p>
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
        <html>
        <head>
            <title>Add Flashcard</title>
            <style>
                body {
                    background: #181a20;
                    color: #e0e0e0;
                    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                    margin: 0;
                    min-height: 100vh;
                }
                h1 {
                    text-align: center;
                    font-weight: 600;
                    margin-top: 40px;
                    color: #fff;
                }
                form {
                    background: #23272f;
                    border-radius: 16px;
                    box-shadow: 0 4px 24px #000a;
                    max-width: 400px;
                    margin: 40px auto;
                    padding: 32px 24px;
                    display: flex;
                    flex-direction: column;
                    gap: 18px;
                }
                label {
                    font-size: 1.05em;
                    color: #00bfae;
                    margin-bottom: 6px;
                }
                input[type="text"] {
                    background: #181a20;
                    color: #e0e0e0;
                    border: 1px solid #333;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 1em;
                    outline: none;
                    transition: border 0.2s;
                }
                input[type="text"]:focus {
                    border: 1.5px solid #00bfae;
                }
                input[type="submit"] {
                    background: #00bfae;
                    color: #181a20;
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 1.1em;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.2s;
                }
                input[type="submit"]:hover {
                    background: #00e6cf;
                }
                .back-link {
                    display: block;
                    text-align: center;
                    margin-top: 24px;
                    color: #00bfae;
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.2s;
                }
                .back-link:hover {
                    color: #00e6cf;
                }
            </style>
        </head>
        <body>
            <h1>Add Flashcard</h1>
            <form method="post">
                <label>Question:</label>
                <input type="text" name="question" required>
                <label>Answer:</label>
                <input type="text" name="answer" required>
                <input type="submit" value="Add">
            </form>
            <a class="back-link" href="{{ url_for('index') }}">&#8592; Back to Flashcards</a>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
