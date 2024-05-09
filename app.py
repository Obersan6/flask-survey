"""
SATISFACTION SURVEY

Keep track of the user's survey responses with a list in the outermost scope in your app.py. 

At the end of the survey, you should have in memory on the server a list that looks like this:
    ['Yes', 'No', 'Less than $10,000', 'Yes']

------------------------------------------------------------------------------------------------
The Root Route

- When the user goes to the root route, render a page that shows the user: the title of the survey, the instructions, and a button to start the survey. 

------------------------------------------------------------------------------------------------
The Question Page

A route that can handle questions:

- It should handle URLs like: 
/questions/0 (the first question),
/questions/1, and so on.

When the user arrives at one of these pages:
- It should show a form asking the current question, 
- and listing the choices as radio buttons. 
- Answering the question should fire off a POST request to '/answer' with the answer the user selected (we'll handle this route next).

Once the user has answered all questions, rather than trying to send them to /questions/5, redirect them to a simple “Thank You!” page.

Once people know the URL structure, it's possible for them to manually go to /questions/3 before they've answered questions 1 and 2. They could also try to go to a question id that doesn't exist, like /questions/7.

- Modify your view function for the question show page to look at the number in the URL and make sure it's correct. 
- If not, you should redirect the user to the correct URL.

------------------------------------------------------------------------------------------------
Flash Messages

Using flash, if the user tries to tinker with the URL and visit questions out of order:

- flash a message telling them they're trying to access an invalid question as part of your redirect.

------------------------------------------------------------------------------------------------
Use Session to store answers for different people

- Modify your start page so that clicking on the button fires off a POST request to a new route that will set session[“responses”] to an empty list. 
- The view function should then redirect you to the start of the survey.
- Then, modify your code so that you reference the session when you're trying to edit the list of responses.
"""


from flask import Flask, request, render_template, redirect, url_for, session, make_response, flash
from flask_debugtoolbar import DebugToolbarExtension 
from surveys import satisfaction_survey


app = Flask(__name__) # Adds a new server (flask app)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# Home route (Survey start page)
@app.route('/')
def survey_startpage():
    """Render a page that shows the user: the title of the survey, the instructions, and a button to start the survey. 

    Use Session to store answers for different people
    """

    # Initialize responses in session
    session['responses'] = []

    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions

    # Render the template with the survey details and start button
    return render_template('survey-instructions.html', survey_title=survey_title, survey_instructions=survey_instructions)

  

# Version  THAT WORKS!!!!!!!!!!!!!!!!!!
@app.route('/questions/<int:question_index>', methods=['POST', 'GET'])
def handle_questions(question_index):
    """This route handles questions:

    - It should handle URLs like: 
    /questions/0 (the first question),
    /questions/1, and so on.

    When the user arrives at one of these pages:
    - It should show a form asking the current question, 
    - and listing the choices as radio buttons. 
    - Answering the question fires off a POST request to '/answer' with the answer the user selected
    
    Once the user has answered all questions, redirect them to a simple “Thank You!” page.
    
    Using flash:
    If the user tries to tinker with the URL and visit questions out of order:
    - flash a message telling them they're trying to access an invalid question as part of your redirect.
    
    Use Session to store answers for different people."""


    responses = session.get('responses', [])

    # Check if user is trying to access a question out of sequence
    if question_index != len(responses):
        # flash a message 'you're trying to access an invalid question'
        flash("You're trying to access an invalid question!")
        # Redirect to the correct question index
        return redirect(url_for('handle_questions', question_index=len(responses)))

    if request.method == 'POST':
        answer = request.form.get('answer')

        if not answer:
            return redirect(url_for('handle_questions', question_index=question_index))
        
        else:
            # Store the answer and proceed
            responses = session['responses']
            responses.append(answer)
            session['responses'] = responses
            print(session['responses'])
            # Check if there are more questions to answer
            if question_index + 1 < len(satisfaction_survey.questions):
                return redirect(url_for('handle_questions', question_index=question_index + 1))
            else:
                # All questions answered, send to a Thank you page
                return "<h1>Thank you!</h1>"

    # If GET request or no form data was submitted, show the current question
    if question_index < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[question_index]
        return render_template('questions.html', question=question, question_index=question_index)
    else:
        return "<h1>Thank you!</h1>"



