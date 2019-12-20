from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
ma = Marshmallow(app)
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id','firstname','lastname','email','password')

person = PersonSchema()
persons = PersonSchema(many=True)



@app.route('/person', methods=["POST"])
def add_person():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    new_person = Person(firstname=firstname,lastname=lastname,email=email,password=password)
    db.session.add(new_person)
    db.session.commit()
    return jsonify(person.dump(new_person))

@app.route('/person', methods=["GET"])
def get_person():
    all_persons = Person.query.all()
    result = persons.dump(all_persons)
    return jsonify(result)

@app.route('/person/<int:id>',methods=["PUT"])
def get_peron(id):
    person_data = Person.query.get(id)
    person_data.firstname = request.json['firstname']
    person_data.lastname = request.json['lastname']
    person_data.email = request.json['email']
    person_data.password = request.json['password']
    db.session.commit()
    return jsonify(person.dump(person_data))

@app.route('/person/<int:id>',methods=["DELETE"])
def person_delete(id):
    person_data = Person.query.get(id)
    db.session.delete(person_data)
    db.session.commit()
    return jsonify(person.dump(person_data))


    


if __name__ == '__main__':
    app.run(debug=True)