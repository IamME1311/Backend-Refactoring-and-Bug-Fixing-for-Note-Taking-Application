# Importing required dependencies
from flask import Flask, render_template, request, redirect, url_for, session
import secrets
app = Flask(__name__) # initializing a Flask object

#  secret key generation
secret_key = secrets.token_hex(16)

app.secret_key = 'secret_key'  # Setting a secret key for session management

user_dictionary = {} # This will be the database of each user on our application, kinda makeshift method

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method=="POST":
        user_name = request.form.get("uname")
        note = request.form.get("note")
        if user_name is not None:
            user_name = user_name.title()  # Convert username to titlecase if it's not None for consistency
        else:
            # Handling the case where 'uname' parameter is not provided in the request URL
            user_name = ""  # Setting an empty string as the username
        if user_name in user_dictionary: # checking if the user exists in our makeshift database
            user_dictionary[user_name].append(note) # if user exists in the database add the notes
        else:
            user_dictionary[user_name] = [note] # if not, create the entry of the user and then add the note since we are adding one note at a time
        session['user_name'] = user_name  # Storing user name in session
        return redirect(url_for('home'))
    else:
        user_name = session.get('user_name', '')  # Retrieve user name from session
        return render_template("home.html", user_dictionary=user_dictionary, user_name=user_name)


if __name__ == '__main__':
    app.run(debug=True)