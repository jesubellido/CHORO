from flask import Flask, render_template, request, redirect, Response, session
import json
from database import connector
from database import entities

app = Flask(__name__)
#app.secret_key = "12345678"
db = connector.Manager()

cache = {}
engine = db.createEngine()


#allusers = session.query(entities.User)


@app.route('/')
def loginpage():
    return render_template('login.html')

@app.route('/loged')
def logedpage():
    return render_template('loged.html')


@app.route('/dologin', methods=['POST'])
def dologin():
    session = db.getSession(engine)
    users = session.query(entities.User)
    data = request.form
    for user in users:
        if user.name == data['username'] and user.password == data['password']:
            return render_template('loged.html')
        else:
            return render_template('login.html')
    return render_template('login.html')



@app.route('/users', methods=['GET'])
def get_users():
    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        users = session.query(entities.User)
        cache[key] = users
        print("From DB")
    else:
        print("From Cache")

    users_list = cache[key]
    response = []
    for user in users_list:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user_single = users.filter(entities.User.id == id)
    for user in user_single:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')
    message = {"status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/users/<id>', methods=['DELETE'])
def remove_user(id):
    deleted_user     = users.filter(entities.User.id == id)
    for user in deleted_user:
        session.delete(user)
    session.commit()
    return "DELETED"


@app.route('/users', methods=['POST'])
def create_user():
    c = request.get_json(silent=True)
    print(c)
    user = entities.User(
        id=c['id'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session.add(user)
    session.commit()
    return 'Created users'


if __name__ == '__main__':
    app.run()
