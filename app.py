from flask import Flask, render_template #Need render_template() to render HTML pages
from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:India_11@localhost/anurag'

app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'FALSE'

db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#this is to elminate storing static and template in cache - only for development point

class employees(db.Model):
  
  id = db.Column('id', db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  division = db.Column(db.String(50))
  Emp_id = db.Column(db.String(100)) 
  Email = db.Column(db.String(100))
  Password = db.Column(db.String(100))
  def __init__(self,name,division,Emp_id,Email,Password):
    self.name = name
    self.division = division
    self.Emp_id = Emp_id
    self.Email = Email
    self.Password = Password
  
@app.route('/')
def home():
  return render_template('home.html')
  
  """Render an HTML template and return"""
  # HTML file to be placed under sub-directory templates

@app.route('/about')
def about():
  return render_template('about.html')
  """Render an HTML template and return"""
   # HTML file to be placed under sub-directory templates


	
@app.route('/login', methods = ['GET', 'POST'] )
def login():
  if request.method == 'POST':
    if not request.form['username'] or not request.form['password']:
      
      flash('Please Enter details', 'error')
    else:
      POST_USERNAME = str(request.form['username'])
      POST_PASSWORD = str(request.form['password'])
      
      query = employees.query.filter(employees.name==POST_USERNAME,employees.Password==POST_PASSWORD)
      result = query.first()
      print (result)
      if result:
        session['logged_in'] = True
        
        return render_template('loginSucess.html')
        #return redirect(url_for('home'))
      else:
        flash('wrong password!')
        
        
  return render_template('login.html')

@app.route('/forgetpasswd', methods = ['GET', 'POST'] )
def forgetpasswd():
  return render_template('forget.html')

@app.route('/forget', methods = ['GET', 'POST'] )
def forget():
  if request.method == 'POST':
    if not request.form['username'] or not request.form['Emp_id'] or not request.form['Email']:
    	
      flash('Please Enter details', 'error')
    else:
      POST_USERNAME = str(request.form['username'])
      POST_EMPID = str(request.form['Emp_id'])
      POST_EMAIL = str(request.form['Email'])
      #return (POST_EMPID)     
      #detail = employees.query.filter(employees.name==POST_USERNAME)
      query = employees.query.filter(employees.name==POST_USERNAME,employees.Emp_id==POST_EMPID)
      result = query.first()
      print (result)
      if result:
          
        return render_template('forgetdetails.html' ,passwd = result.Password)
        #return redirect(url_for('home'))
      else:
        flash('wrong details!')
  return render_template('forget.html')    
      #return(result.Email)



@app.route('/signup', methods = ['GET', 'POST'] )
def signup():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['division'] or not request.form['Emp_id'] :
        flash('Please enter all the fields', 'error')
      else:
         employee = employees(request.form['name'], request.form['division'],
            request.form['Emp_id'], request.form['Email'],request.form['Password'])
         
         db.session.add(employee)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('login'))
   return render_template('signup.html')
 
if __name__ == '__main__':
	
  db.create_all()
  app.run(debug=True) # Enable reloader and debugger