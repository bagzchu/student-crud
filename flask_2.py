# type: ignore
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/practice_1"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = True)

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

student_schema = StudentSchema()
students_schema = StudentSchema(many = True)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/students", methods = ["POST"])
def add_students():
    req_data = request.get_json()
    student = Student(name = req_data["name"], age = req_data["age"])
    db.session.add(student)
    db.session.commit()
    return {"message": "Congrats! Successfully Added"}

@app.route("/students", methods = ["GET"])
def get_students():
    students = Student.query.all()
    return students_schema.dump(students)

@app.route("/students/<int:student_id>", methods = ["GET"])
def get_student(student_id):
    student = Student.query.get(student_id)
    return student_schema.dump(student)

app.run(debug = True)