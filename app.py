from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

"""Initializing flask app"""
app = Flask(__name__)

"""For ORM Querry i have made use of SQLAlchmey"""
db = SQLAlchemy()
ma = Marshmallow()
mySql = MySQL(app)

"""Created a model for storing data"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    aadhaar_number = db.Column(db.String(12))
    unique_id = db.Column(db.String(10))

    def __init__(self, first_name, aadhaar_number, unique_id):
        self.first_name = first_name
        self.aadhaar_number = aadhaar_number
        self.unique_id = unique_id

"""Setting databaseConnection"""

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:anamroot@localhost/mydb"
db.init_app(app)

"""Creating table its like applying migration for the model to create a table"""
with app.app_context():
    db.create_all()

"""Logic"""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        aadhaar_number = request.form['aadhaar_number']

        # Generate a unique ID using first name and Aadhaar number
        unique_id = first_name[:3].upper() + aadhaar_number[-4:]

        user_data = User(first_name =first_name , aadhaar_number=aadhaar_number , unique_id=unique_id)
        db.session.add(user_data)
        db.session.commit()

        return render_template('data.html', unique_id=unique_id)
    
    return render_template('index.html')


"""Fetching all data from the model"""
@app.route('/allusers')
def users():
    all_users = User.query.all()
    print("------------allusrrs", all_users)
    return render_template('users.html', users=all_users)



if __name__ == "__main__" :
    app.run(debug = True)


