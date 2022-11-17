from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://bun:bun@cluster0.a94hsbx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html');


@app.route('/index')
def indexHtml():
    return render_template('index.html');


# @app.route('/')
# def p4_home():
#     return render_template('p4_index.html')


@app.route("/p4_user", methods=["POST"])
def p4_user_post():
    p4_name_receive = request.form['p4_name_give']
    p4_comment_receive = request.form['p4_comment_give']

    p4_user_list = list(db.p4_user.find({}, {'_id': False}))
    p4_count = len(p4_user_list) + 1

    doc = {
        'p4_num': p4_count,
        'p4_name': p4_name_receive,
        'p4_comment': p4_comment_receive,
        'p4_done': 0
    }

    db.p4_user.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


@app.route("/p4_user", methods=["GET"])
def p4_user_get():
    p4_comment_list = list(db.p4_user.find({}, {'_id': False}))
    return jsonify({'p4_comments': p4_comment_list})


@app.route("/p4_user/p4_done", methods=["POST"])
def p4_delete_comment():
    p4_num_receive = request.form['p4_num_give']
    db.p4_user.update_one({'p4_num': int(p4_num_receive)}, {'$set': {'p4_done': 1}})
    return jsonify({'msg': '삭제 완료'})


@app.route('/introduce')
def introduceHtml():
    return render_template('introduce.html');


@app.route('/more')
def moreHtml():
    return render_template('more.html');


@app.route('/individual/p2')
def p2home():
    return render_template('/individual/p2.html')


@app.route('/individual/p3')
def p3Html():
    return render_template('individual/p3.html');


@app.route('/individual/p3Test')
def p3TestHtml():
    return render_template('individual/p3Test.html');


@app.route("/p2_comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    doca = {
        'comment': comment_receive,
    }
    db.p2_comment.insert_one(doca)
    return jsonify({'msg': '입력 완료!'})


@app.route("/p2_comment", methods=["GET"])
def comment_get():
    comment_list = list(db.p2_comment.find({}, {'_id': False}))
    return jsonify({'comment': comment_list})


@app.route('/comment', methods=['GET'])
def comment_get():
    allComments = list(db.comments.find({}, {'_id': False}));

    return jsonify({'result': 'success', 'allComments': allComments, 'msg': '수신 완료'});


@app.route('/comment', methods=['POST'])
def comment_post():
    comment_receive = request.form['comment_give']
    hour_receive = request.form['hour_give']
    minute_receive = request.form['minute_give']

    allComments = list(db.comments.find({}, {'_id': False}));
    commentsLength = len(allComments);

    if commentsLength == 0:
        num = 0;
    else:
        num = allComments[commentsLength - 1]['num'] + 1;

    doc = {
        'comment': comment_receive,
        'hour': int(hour_receive),
        'minute': int(minute_receive),
        'num': num

    }

    db.comments.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '작성 완료!'})


@app.route('/comment/delete', methods=['POST'])
def comment_delete():
    num_receive = request.form['num_give']

    db.comments.delete_one({'num': int(num_receive)});

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})

# p0 강성주 app.py

# 방명록 작성
@app.route('/p0_guestBook', methods=['POST'])
def write_guestbook():
    name_receive = request.form['name_give']
    content_receive = request.form['content_give']

    doc = {
        'name': name_receive,
        'content': content_receive,
        'likes': 0
    }

    db.p0.insert_one(doc)

    return jsonify({'msg': '저장완료!'})

# 방명록 불러오기

@app.route('/p0_guestBook', methods=['GET'])
def read_guestbook():
    comment = list(db.p0.find({}, {'_id': False}))
    return jsonify({'all_contents': comment})

# 방명록 삭제

@app.route('/p0_delete', methods=['POST'])
def delete_comment():
    name_receive = request.form['name_give']
    db.p0.delete_one({'name': name_receive})
    return jsonify({'msg': '삭제 완료!'})

# @app.route('/mypage')
# def mypage():
#    return '<button>나는버튼이다</button>';


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
