from flask import Flask, render_template, request, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

# Set the secret key to enable the Flask Debug Toolbar
app.config['SECRET_KEY'] = 'oh-so-secret'

# Enable the Flask Debug Toolbar
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize the responses list
responses = []

@app.route("/")
def start_survey():
    #Pass survey title and instruction to the template
    return render_template("start.html", survey=satisfaction_survey)

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    global responses  # Add this line to access the global variable

    if len(responses) == len(satisfaction_survey.questions):
        flash('Survey completed. Thank you!','success')
        return redirect(url_for('thank_you'))

    if question_id != len(responses):
        return redirect(url_for('question', question_id=len(responses)))

    if request.method == 'POST':
        try:
            response = request.form['choice']
            responses.append(response)
            if len(responses) == len(satisfaction_survey.questions):
                return redirect(url_for('thank_you'))
            else:
                return redirect(url_for('question', question_id=len(responses)))
        except KeyError:
            flash('Please select a choice before proceeding.', 'error')
            return redirect(url_for('question', question_id=len(responses)))

    return render_template('question.html', question=satisfaction_survey.questions[question_id], question_id=question_id)


@app.route('/thank-you')
def thank_you():
    # Render a thank-you page
    return render_template('thank_you.html', responses=responses)