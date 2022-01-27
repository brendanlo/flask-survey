from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
responses = []

@app.get('/')
def survey_start():

  survey_title = survey.title
  survey_instructions = survey.instructions
  
  return render_template("survey_start.html", title = survey_title, 
  instructions = survey_instructions)

@app.post('/begin')
def redirect_to_questions():
    return redirect("/questions/0")

@app.get('/questions/<question_num>')
def get_question(question_num):
    question_instance = survey.questions[int(question_num)] #TODO: why doesnt int typecast work in decorator
    question = question_instance.question
    choices = question_instance.choices
    allow_text = question_instance.allow_text
    return render_template("question.html", question=question, choices=choices, allow_text=allow_text)


