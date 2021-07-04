from flask import Flask, render_template, url_for, request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
#config database location using SQLITE relative path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app) #initialize database

#create a model
class Todo(db.Model): # Todo name of DB
    # creates ID for each entry
    id= db.Column(db.Integer,primary_key=True)
    content= db.Column(db.String(150),nullable=False)

    # set time automatically
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        
# Maun entry point
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        #request is equal to "content" from index.html input tag
        task_content = request.form.get("sumText")
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "Issue updating your list"
    else:
        # sort DB by order created and return items
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "Issue delete task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)



if __name__ =="__main__":
    app.run(debug=True)