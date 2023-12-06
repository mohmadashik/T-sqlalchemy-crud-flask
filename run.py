from flask import jsonify,request
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://amohmad:welcome@localhost:3306/example'
db  = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(250),unique=True)

@app.route('/')
def home():
    return 'hello world'


@app.route('/view')
def view():
    all_data = User.query.all()
    all_users = {}
    for user in all_data:
        all_users[user.id] = {'name':user.name,'age':user.age,'email':user.email}
    return jsonify({'all_data':all_users})

@app.route('/add',methods=['POST'])
def add():
    data = request.json
    name = data.get('name')
    age = data.get('age',16)
    email = data.get('email',f'{name}@mail.com')
    user_obj = User(name=name,age=age,email=email)
    db.session.add(user_obj)
    db.session.commit()
    return 'user object added successfully!'

@app.route('/update',methods=['PUT'])
def update() : 
    data = request.json
    id = data.get('id')
    user_obj = User.query.filter_by(id=id).first()
    new_name = data.get('name',user_obj.name)
    new_age = data.get('age',user_obj.age)
    new_email = data.get('email',user_obj.email)
    user_obj.name = new_name
    user_obj.age = new_age
    user_obj.email = new_email
    db.session.commit()
    return 'object updated succesfully'


@app.route('/delete',methods=['DELETE'])
def delete():
    data = request.json
    delete_id = data.get('id')
    delete_user_obj = User.query.filter_by(id=delete_id).first()
    db.session.delete(delete_user_obj)
    db.session.commit()
    return f'object of id {delete_id} is deleted'


with app.app_context():
    db.create_all()


if __name__=='__main__':
    app.run(debug=True)

