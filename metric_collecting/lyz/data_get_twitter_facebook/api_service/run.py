from flask import Flask, render_template, request
from flask import jsonify
import pymysql
import json
host = "39.106.16.105"
user = "root"
password = "123456"
name_db = "trajectory"
conn = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=name_db, charset='utf8')
conn.autocommit(1)
cur = conn.cursor()
app = Flask(__name__)


app.config['SECRET_KEY'] = "dfdfdffdad"


@app.route('/')
def index():
    return render_template('traj.html')

@app.route('/mystring',methods=['GET','POST'])
def mystring():
    data=request.json
    query_sql="select * from stay_point where user_id=%d"
    cur.execute(query_sql%(int(data['user_id'])))
    res=cur.fetchall()
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
