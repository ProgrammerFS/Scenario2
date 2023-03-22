from flask import Flask, request, make_response, send_file, render_template, redirect, send_from_directory, session
import io
from flask_session import Session
import base64
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib_venn import venn2, venn2_circles
import json

global index
index = 0
global pulled
pulled = 0
global x
x = {}
global l
l = []
global answers
answers = []


app = Flask(__name__)
matplotlib.use('Agg')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_users():
    users = {}
    with open('users.txt') as f:
        for line in f:
            username, password = line.strip().split(':')
            users[username] = password
    return users

def write_users(username, password):
    with open('users.txt',"a") as f:
        f.write(f"{username}:{password}\n")
    return "written"

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/student")
def student():
    if session["name"]!=False:
        return render_template("student.html")
    else:
        return redirect("/login")

@app.route('/visualization', methods=['GET','POST'])
def generate_venn_diagram():
    if session["name"]!=False:
        if request.method == "GET":
            return render_template("visualization.html")
        else:
            setA = request.form["setA"]
            setB = request.form["setB"]
            setRelation = request.form["setRelation"]
            setA_values = set(setA.split(","))
            setB_values = set(setB.split(","))
            fig, ax = plt.subplots()
            if setRelation == "intersection" or setRelation=="union":
                venn2([setA_values, setB_values])
            elif setRelation == "differenceAB":
                venn2([setA_values - setB_values, setB_values], set_colors=('#4F9D9D', '#F1948A'), set_labels=('Set A - Set B', 'Set B'), ax=ax)
            elif setRelation == "differenceBA":
                venn2([setA_values, setB_values - setA_values], set_colors=('#4F9D9D', '#F1948A'), set_labels=('Set A', 'Set B - Set A'), ax=ax)

            filename = 'venn1.png'
            filepath = os.path.join('static', 'img', filename)
            fig.savefig(filepath, format='png')
            plt.clf()
            return render_template("visualized.html")
    else:
        return redirect("/login")

@app.route("/student/quiz", methods=["GET", "POST"])
def quiz():
    global pulled, x, l, index,answers
    if session["name"]!=False:
        if request.method == "GET":
            
            if pulled==0:
                pulled = 1
                f = open("./questions/1.json")
                data = json.load(f)
                for i in data["questions1"]:
                    for j in i:
                        l.append(j)
                        x[j] = i[j]
                question = l[index]
                options = x[question]
                return render_template("quiz.html", q = question, options = options)
            else:
                if index < len(l) or index == 0:
                    question = l[index]
                    options = x[question]
                    return render_template("quiz.html", q = question, options = options)
                else:
                    incorrect = []
                    fa = open("./questions/answers.json")
                    data = json.load(fa)
                    if data["answers"] != answers:
                        for i in data["answers"]:
                            if i not in answers:
                                incorrect.append(i)
                    # if incorrect!=[]:
                    #     return render_template("incorrect.html")
                    return "Thank You"
        if request.method == "POST":
            if index < len(l) or index == 0:
                answer = request.form["answer"]
                answers.append(answer)
                print("answer :", answer)
                index+=1
                return redirect("/student/quiz")
    else:
        return redirect("/login")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if session["name"]!=False:
        if request.method == "GET":
            return render_template("question_upload.html")
        else:
            form = request.form
            question = form.get("question")
            option1 = form.get("option1")
            option2 = form.get("option2")
            option3 = form.get("option3")
            option4 = form.get("option4")
            answer = form.get("answer")
            fa = open("./questions/answers.json")
            answers = json.load(fa)
            answers["answers"].append(answer)
            fa.close()
            fa = open("./questions/answers.json", "w")
            answer_obj = json.dumps(answers)
            fa.write(answer_obj)
            fa.close()
            f = open("./questions/1.json")
            data = json.load(f)
            d = {question : [option1, option2, option3, option4]}
            data["questions1"].append(d)
            f.close()
            f = open("./questions/1.json", "w")
            data_obj = json.dumps(data)
            f.write(data_obj)
            f.close()
            return render_template("question_upload.html")
    else:
        return redirect("/login")


@app.route("/visualization")
def visualization():
    if session["name"]!=False:
        return render_template("visualization.html")
    else:
        return redirect("/login")

@app.route("/cheatsheet")
def hello():
    if session["name"]!=False:
        return render_template("cheatsheet.html")
    else:
        return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username not in users or users[username] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            session["name"] = username
            session["isloggedin"] = True
            return redirect("/")
    return render_template('login.html', error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form["c_password"]
        if confirm_password!=password:
            return render_template("signup.html", message="Passwords don't match")
        elif username in get_users():
            return render_template("signup.html", message="Username is in use")
        else:
            write_users(username, password)
            return redirect("/")

    return render_template('signup.html',  message = None)

@app.route("/logout")
def logout():
    session["name"] = False
    return "Logged out succesfully"

if __name__ == '__main__':
    app.run(port=9889, debug = True)

