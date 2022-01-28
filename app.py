from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from surveys import satisfaction_survey as survey
from surveys import personality_quiz as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def survey_start():
    """Renders survey start page and initializes session cookies responses & 
    current_question"""

    # can check len(session['responses']) to check the right question. could put the reset values in the begin route
    session['responses'] = []
    session['current_question'] = 0

    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=survey_title,
        instructions=survey_instructions)


@app.post('/begin')
def redirect_to_questions():
    """Redirect from start page to questions/0"""

    return redirect("/questions/0")


@app.get('/questions/<int:question_num>')
def get_question(question_num):
    """Render question page and prevents users from accessing questions that 
    are not valid"""

    # if user tries to directly access a question, but has completed the survey,
    # they will be redirected to the completion page
    if (session['current_question'] == len(survey.questions)):
        flash("You've already completed the survey, thanks!")
        return redirect('/completion')

    # if user tries directly accessing a question out of order, they will be
    # redirected to their correct question page
    elif (question_num != session['current_question']):
        print("Redirecting to current page")
        flash(
            "You were trying to access an invalid question, please answer this one")
        return redirect(f"/questions/{session['current_question']}")

    # can clean this up by passing the question instance directly to Jinja
    question_instance = survey.questions[question_num]
    question = question_instance.question
    choices = question_instance.choices
    allow_text = question_instance.allow_text

    return render_template(
        "question.html",
        question=question,
        choices=choices,
        allow_text=allow_text,
        question_num=question_num)


@app.post('/answer')
def add_response_and_redirect():
    """Store user answer in responses.
    If last question, redirect to competion page.
    Else, increment question number and redirect next question page"""

    session['current_question'] += 1

    responses = session['responses']

    # stores data into session['responses']
    if request.form.get('text_answer'):
        responses.append(
            {request.form['answer']: request.form['text_answer']})
    else:
        responses.append(request.form['answer'])

    # rebinding triggers session to save the updated values
    session['responses'] = responses

    # directing user to the correct page
    if (session['current_question'] == len(survey.questions)):
        return redirect('/completion')
    else:
        return redirect(f"questions/{session['current_question']}")


@app.get('/completion')
def thank_user():
    """Render completion page"""

    return render_template("completion.html")
