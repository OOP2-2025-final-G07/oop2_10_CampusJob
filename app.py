from flask import Flask, render_template
from models import initialize_database, User
from models.registration import Registration
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

# ★ 時給分布グラフ用ルート
@app.route("/graph/hourly_wage")
def wage_graph():
    regs = Registration.select().join(User)

    bins = [
        "~1,100", "~1,150", "~1,200", "~1,250", "~1,300",
        "~1,350", "~1,400", "~1,450", "~1,500", "~1,550",
        "~1,600", "1,600~"
    ]

    grades = ["1", "2", "3", "4"]

    # 学年 × 時給帯 の初期化
    data = {
        grade: {b: 0 for b in bins}
        for grade in grades
    }

    def wage_bin(w):
        if w <= 1100: return "~1,100"
        elif w <= 1150: return "~1,150"
        elif w <= 1200: return "~1,200"
        elif w <= 1250: return "~1,250"
        elif w <= 1300: return "~1,300"
        elif w <= 1350: return "~1,350"
        elif w <= 1400: return "~1,400"
        elif w <= 1450: return "~1,450"
        elif w <= 1500: return "~1,500"
        elif w <= 1550: return "~1,550"
        elif w <= 1600: return "~1,600"
        else: return "1,600~"

    for r in regs:
        grade = r.user.grade
        if grade not in grades:
            continue
        b = wage_bin(r.hourly_wage)
        data[grade][b] += 1

    return render_template(
        "graphs/hourly_wage.html",
        labels=bins,
        datasets=data
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

