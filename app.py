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

@app.route('/introduce')
def introduceHtml():
   return render_template('introduce.html');

@app.route('/more')
def moreHtml():
   return render_template('more.html');


@app.route('/p2')
def p2home():
   return render_template('p2.html')


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
    return jsonify({'msg':'입력 완료!'})

@app.route("/p2_comment", methods=["GET"])
def comment_get():
    comment_list = list(db.p2_comment.find({}, {'_id': False}))
    return jsonify({'comment':comment_list})


@app.route('/comment', methods=['GET'])
def comment_get():

   allComments = list(db.comments.find({}, {'_id': False}));

   return jsonify({'result':'success', 'allComments': allComments, 'msg':'수신 완료'});


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
      num = allComments[commentsLength-1]['num'] + 1;


   doc = {
      'comment' : comment_receive,
      'hour' : int(hour_receive),
      'minute' : int(minute_receive),
      'num' : num

   }

   db.comments.insert_one(doc)


   return jsonify({'result':'success', 'msg': '작성 완료!'})


@app.route('/comment/delete', methods=['POST'])
def comment_delete():
   num_receive = request.form['num_give']


   db.comments.delete_one({'num':int(num_receive)});


   return jsonify({'result':'success', 'msg': '삭제 완료!'})



# @app.route('/mypage')
# def mypage():
#    return '<button>나는버튼이다</button>';


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)