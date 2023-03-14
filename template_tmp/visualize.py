from flask import Flask, request, make_response, send_file
import io
import base64
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib_venn import venn2, venn2_circles
matplotlib.use('Agg')

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(port=9889)

