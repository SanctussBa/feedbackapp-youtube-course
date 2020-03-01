from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app = Flask(__name__)


# heroku will have anothere database so we have to create statement which define
# when it's under deployment and when under development mode
#ENV = 'dev'
if ENV == 'dev':
    # If its under development mode... then:
    app.debug = True
    # configure postgres database  we wanna set it to postgresql://username:password@localhost/databasename
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:berzone@localhost/lexus'
else:
    # else its under deployment/production mode
    app.debug = False
    # configure production database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bvtnsvwfxstzqh:c24dec1def00d415d3fb18222a0ea803b77ae56f174072e9e80d5d256fd57879@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d527vfs9e7kg8c' #This only we get during deployment to heroku where we create database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# sql works in a way of modeels. So we have to create model by defining class

class Feedback(db.Model):
    __tablename__ = 'feedback' #we set name of the table
    # now we wanna define our fields
    id = db.Column(db.Integer, primary_key=True)#it's gonna be integer and primary key is True
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments): #all except id
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

# Now we should be able to make querries to our database


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # To make shure that this is post request only
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']

        # To make sure that user enters customer and dealer fields
        if customer == '' or dealer =='':
            return render_template('index.html', message='Please enter required fields')

        # lets make check that only one custumer can submit only one feedback and not more.
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            # basically we count customers and if customer is ZERO menaing it does not exist
            data = Feedback(customer, dealer, rating, comments)# we make an instance of model
            db.session.add(data)
            db.session.commit()#new data will be saved in database

            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')# return success page if all good
        return render_template('index.html', message='You have already submitted feedback')

if __name__ == '__main__':

    app.run()
