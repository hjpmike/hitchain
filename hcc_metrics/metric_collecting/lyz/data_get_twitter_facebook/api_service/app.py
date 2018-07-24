from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request


app = Flask(__name__)
access_token = [
    '123456',
    '654321'
]

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

all_ranking_result = []
each_prj_ranking_result = {}

def get_each_prj_ranking_result():

    prj_id, prj_name, git_url, coin, rank_date, \
    rank, score, metric_1, metric_2, metric_3,\
    metric_4, metric_5, metric_6 = 1, "coin", "sdf", "asd", "2018", 1, 1, 1, 1, 1, 1, 1, 1

    return prj_id, prj_name, git_url, coin, rank_date, rank, score, metric_1, metric_2, metric_3, metric_4, metric_5, metric_6

def get_each_prj_ranking_result(start_time, end_time):

    prj_id, prj_name, git_url, coin, rank_date, \
    rank, score, metric_1, metric_2, metric_3,\
    metric_4, metric_5, metric_6 = 1, "coin", "sdf", "asd", "2018", 1, 1, 1, 1, 1, 1, 1, 1

    return prj_id, prj_name, git_url, coin, rank_date, rank, score, metric_1, metric_2, metric_3, metric_4, metric_5, metric_6




@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/coin/api/all_ranking', methods=['GET'])
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_all_ranking():
    try:
        for re_arg in request.args:

            if request.args[re_arg] in access_token:

                # 返回所有项目排行列表


                return 'u are so beautiful'
            else:
                abort(404)
    except:
        abort(404)


@app.route('/prj_ranking',methods=['GET'])
def get_prj_ranking():
    try:
        prj_id = request.args['prj_id']
        start_time = request.args['start_time']
        end_time = request.args['end_time']
        # 防止有多的参数
        for re_arg in request.args:
            if 'prj_id' == re_arg or 'start_time' == re_arg or 'end_time' == re_arg:
                # 返回列表

                return prj_id + start_time + end_time
            else:
                abort(404)
    except:
        abort(404)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(debug=True)