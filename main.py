from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connect to MongoDB
client = MongoClient("mongodb+srv://admin:JAAV@cluster0.ehuqcdb.mongodb.net/logins?retryWrites=true&w=majority&appName=Cluster0")
db = client.logins
users_collection = db.users

# Function to create the default admin user
def create_admin():
    admin_email = 'admin@example.com'
    admin_password = 'adminpassword'
    
    # Check if admin user already exists
    if not users_collection.find_one({"email": admin_email}):
        users_collection.insert_one({"email": admin_email, "password": admin_password})
        print("Default admin user created.")

# Create the default admin user if not exists
create_admin()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    user = users_collection.find_one({"email": email})
    if user and user["password"] == password:
        session['email'] = email  # Storing email in session
        return redirect(url_for('signed_in'))
    else:
        return render_template('incorrect.html')

@app.route('/signedin')
def signed_in():
    email = session.get('email')
    if email:
        return render_template('signedin.html', email=email)
    else:
        return redirect(url_for('index'))  # Redirect to login page if email not in session

@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    email = session.get('email')
    if email:
        # Handle document upload process here using the 'email' variable
        return redirect(url_for('documents'))
    else:
        return redirect(url_for('index'))  # Redirect to login page if email not in session

@app.route('/recommendations')
def recommendations():
    email = session.get('email')
    if email:
        # Dummy data for recommendations
        job_links = [
            {"title": "Job 1", "link": "https://example.com/job1"},
            {"title": "Job 2", "link": "https://example.com/job2"}
        ]
        house_links = [
            {"title": "House 1", "link": "https://example.com/house1"},
            {"title": "House 2", "link": "https://example.com/house2"}
        ]
        return render_template('recommendations.html', job_links=job_links, house_links=house_links)
    else:
        return redirect(url_for('index'))  # Redirect to login page if email not in session

@app.route('/documents')
def documents():
    email = session.get('email')
    if email:
        return render_template('documents.html')
    else:
        return redirect(url_for('index'))  # Redirect to login page if email not in session

if __name__ == '__main__':
    app.run(debug=True)
