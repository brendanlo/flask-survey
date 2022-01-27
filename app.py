from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from surveys import satisfaction_survey as survey
from surveys import personality_quiz as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
responses = []

@app.get('/')
def survey_start():
    """Renders survey start page"""

    survey_title = survey.title
    survey_instructions = survey.instructions
  
    return render_template(
        "survey_start.html", 
        title = survey_title, 
        instructions = survey_instructions)

@app.post('/begin')
def redirect_to_questions():
    """Redirect from start page to questions/0"""

    return redirect("/questions/0")

@app.get('/questions/<int:question_num>')
def get_question(question_num):
    """Render question page"""

    question_instance = survey.questions[question_num] 
    question = question_instance.question
    choices = question_instance.choices
    allow_text = question_instance.allow_text
    print(f"allow text {allow_text}")

    return render_template(
        "question.html", 
        question=question, 
        choices=choices, 
        allow_text=allow_text, 
        question_num = question_num)

@app.post('/answer')
def add_response_and_redirect():
    """Store user answer in responses.
    If last question, redirect to competion page.
    Else, increment question number and redirect next question page"""

    if request.form.get('text_answer'):
        responses.append({request.form['answer'] : request.form['text_answer']})
    else:
         responses.append(request.form['answer'])

    question_num = int(request.form['question_num']) + 1

    if question_num == len(survey.questions):
        return redirect('/completion')
    else:
        return redirect(f"questions/{question_num}")


@app.get('/completion')
def thank_user():
    """Render completion page"""
    print(responses)
    return render_template("completion.html")