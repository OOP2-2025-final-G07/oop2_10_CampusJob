from flask import Flask, render_template
from models import initialize_database
from models.registration import Registration
from models import Registration, Job 
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    return render_template('index.html')

from flask import render_template

#@app.route("/graph/<name>")
#def graph(name):
#    return render_template(f"graphs/{name}.html")
@app.route('/multi-job-holders')
def multi_job_holders():
    # Registration モデルを使用してデータを取得
    registrations = Registration.select()
    
    # templates/graphs/ フォルダの中にある HTML を指定
    return render_template('graphs/Multi-job_holders.html', registrations=registrations)
# ★ 時給分布グラフ用ルート
@app.route("/graph/hourly_wage")
def wage_graph():
    regs = Registration.select()

    bins = {
        "~1,100": 0,
        "~1,150": 0,
        "~1,200": 0,
        "~1,250": 0,
        "~1,300": 0,
        "~1,350": 0,
        "~1,400": 0,
        "~1,450": 0,
        "~1,500": 0,
        "~1,550": 0,
        "~1,600": 0,
        "1,600~": 0,
    }

    for r in regs:
        w = r.hourly_wage
        if w <= 1100:
            bins["~1,100"] += 1
        elif w <= 1150:
            bins["~1,150"] += 1
        elif w <= 1200:
            bins["~1,200"] += 1
        elif w <= 1250:
            bins["~1,250"] += 1
        elif w <= 1300:
            bins["~1,300"] += 1
        elif w <= 1350:
            bins["~1,350"] += 1
        elif w <= 1400:
            bins["~1,400"] += 1
        elif w <= 1450:
            bins["~1,450"] += 1
        elif w <= 1500:
            bins["~1,500"] += 1
        elif w <= 1550:
            bins["~1,550"] += 1
        elif w <= 1600:
            bins["~1,600"] += 1
        else:
            bins["1,600~"] += 1

    return render_template(
        "graphs/hourly_wage.html",
        labels=list(bins.keys()),
        values=list(bins.values())
    )



@app.route("/graph/occupation")
def occupation_graph():
    regs = Registration.select().join(Job)

    counts = {
        "飲食": 0,
        "事務": 0,
        "小売": 0,
        "作業": 0,
        "教育": 0,
        "マスコミ": 0,
        "エンタメ": 0,
        "在宅": 0,
        "その他": 0
    }

    for r in regs:
        counts[r.job.occupation] += 1

    return render_template(
        "graphs/chart_occupation.html",
        labels=list(counts.keys()),
        values=list(counts.values())
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

