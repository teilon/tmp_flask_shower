from flask import Flask, render_template, send_file
from flask_sqlalchemy import SQLAlchemy

import pandas as pd

from config import SQLALCHEMY_DATABASE_URI
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/", methods=['POST', 'GET'])
def hello():
    return render_template('index.html')


class Sino_trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    station = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    sale = db.Column(db.Integer, default=0)
    rest = db.Column(db.Integer, default=0)
    month = db.Column(db.String(50), nullable=False)
    aroma_type = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/month")
def month():
    sql = 'select distinct month from sino_trade;'
    df = pd.read_sql(sql, db.engine)
    print(df)
    return render_template('month.html', data=df['month'])


import matplotlib.pyplot as plt
import seaborn as sb
from io import BytesIO


@app.route("/calc")
def calc():
    return render_template('calc.html')


@app.route('/donut_pie_chart/')
def donut_pie_chart():
    sql = 'select station, number, sale ' \
          'from sino_trade ' \
          'where region=\'Актау\' ' \
          'and month=\'nov\';'
    df = pd.read_sql(sql, db.engine)

    #----------------------------------
    sb.set_style('whitegrid')
    plt.plot(df['sale'])

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    #----------------------------------

    #----------------------------------
    # sb.set_style('whitegrid')
    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    # ax.plot(df['sale'])

    # img = BytesIO()
    # fig.savefig(img)
    # img.seek(0)
    #----------------------------------

    return send_file(img, mimetype='image/png')


@app.route("/chart")
def chart():
    #----------------------------------
    # legend = 'Monthly Data'
    # labels = ['January', 'February', 'March',
    #            'April', 'May', 'June',
    #            'July', 'August']
    # values = [10, 9, 8, 7, 6, 4, 7, 8]
    # return render_template('chart.html', values=values, labels=labels, legend=legend)
    # ----------------------------------

    legend = 'Monthly Data'
    sql = 'select station, number, sale ' \
          'from sino_trade ' \
          'where region=\'Актау\' ' \
          'and month=\'nov\';'
    df = pd.read_sql(sql, db.engine)
    return render_template('chart.html',
                           values=df['sale'],
                           labels=df['station'],
                           legend=legend
                           )


if __name__ == '__main__':
    app.run(port=5000)
