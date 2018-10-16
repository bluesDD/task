# coding: UTF-8

import flask
from google.appengine.ext import ndb


###Flaskインスタンスの作成
app = flask.Flask(__name__)


###DBに保存するデータのクラスを定義
class User(ndb.Model):
    """
    name, mail, passwordの3つのProertyを用意する
    """
    name = ndb.StringProperty()
    mail = ndb.StringProperty()
    password = ndb.StringProperty()


###ルーティングの設定
#トップページの設定
@app.route('/')
def toppage():
    return flask.render_template('toppage.html')

#shownameページの設定
@app.route('/showname')
def showname():
    name = flask.request.args['name']
    return flask.render_template('showname.html', name=name)

#newページの設定
#POSTリクエストを送信した際に新データを保存
@app.route('/database/new', methods=['POST'])
def database_new():
    #リクエストを変数化
    name = flask.request.form['name']
    mail = flask.request.form['mail']
    password = flask.request.form['password']
    user = User(name=name, mail=mail, password=password)
    #datastoreに保存
    user.put()

#getページの設定
#POSTリクエストで受け取ったusernameと、passwordが正しい場合アドレスを返す
#間違っている場合、エラーメッセージを返す
@app.route('/database/get', methods=["POST"])
def database_get():
    #リクエストを変数化
    name = flask.request.form['name']
    password = flask.request.form['password']
    #変数をクエリでdatastoreに投げる
    query = User.query(ndb.AND(User.name == name, User.password == password))
    #クエリ結果を変数化、合致しない場合Noneが返る
    result = query.get()
    if result is None:
        return 'ユーザーネームとパスワードの組み合わせが正しくないです。'
    else:
        #None以外で、変数mailを取得
        return result.mail

#refleshページの設定
#getで取得した変数を新しく代入してputでDatastoreに戻す
@app.route('/database/reflesh', methods=['POST'])
def databse_reflesh():
    username = flask.request.form['user']
    user_entity = User.query(User.name == username).get()
    #有効でないEntityが帰ってきた場合分け
    if user_entity:
        for key, value in flask.request.form.items():
            if key != 'user':
                if setattr(user_entity, key):
                    setattr(user_entity, key, value)
        user_entity.put()
    else:
        return '該当するユーザーが見つかりませんでした'