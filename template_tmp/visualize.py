from flask import Flask, request, make_response, send_file, render_template, redirect, send_from_directory
import io
import base64
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib_venn import venn2, venn2_circles
import json
matplotlib.use('Agg')
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

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/student")
def student():
    return render_template("student.html")

@app.route('/generate_venn_diagram', methods=['GET','POST'])
def generate_venn_diagram():
    # 从HTTP请求中获取参数
    setA = request.args.get('setA', '')
    setB = request.args.get('setB', '')
    setRelation = request.args.get('setRelation', 'intersection')

    # 解析Set A和Set B
    setA_values = set(setA.split(","))
    setB_values = set(setB.split(","))

    # 根据Set Relation绘制Venn图表
    fig, ax = plt.subplots()
    if setRelation == "intersection":
        venn2([setA_values, setB_values], set_colors=('#4F9D9D', '#F1948A'), set_labels=('Set A', 'Set B'), ax=ax)
    elif setRelation == "union":
        venn2([setA_values, setB_values], set_colors=('#4F9D9D', '#F1948A'), set_labels=('Set A', 'Set B'), alpha=0.5, ax=ax)
    elif setRelation == "differenceAB":
        venn2([setA_values - setB_values, setB_values], set_colors=('#4F9D9D', '#F1948A'), set_labels=('Set A - Set B', 'Set B'), ax=ax)
    elif setRelation == "differenceBA":
        venn2([setA_values, setB_values - setA_values], set_colors=('#4F9D9D', '#F1948A'), set_labels=('Set A', 'Set B - Set A'), ax=ax)

    # 保存图像到静态文件夹中
    os.makedirs('static/images', exist_ok=True)
    filename = 'venn.png'
    filepath = os.path.join('static', 'images', filename)
    fig.savefig(filepath, format='png')

    # 清空图表以释放内存
    plt.clf()

    # 构造包含图像的HTML代码
    image_html = f'<img src="/{filepath}" alt="venn diagram">'

    # 将图像添加到HTTP响应中
    response = make_response(image_html)
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route("/student/quiz", methods=["GET", "POST"])
def quiz():
    global pulled, x, l, index,answers
    
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


@app.route("/upload", methods=["GET", "POST"])
def upload():
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


@app.route("/visualization")
def visualization():
    return render_template("visualization.html")

@app.route("/cheatsheet")
def hello():
    return render_template("cheatsheet.html")

if __name__ == '__main__':
    app.run(port=9889, debug = True)

