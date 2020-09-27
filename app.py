from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)           # initializing flask app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
db = SQLAlchemy(app)

class Todo(db.Model):               # data base table class used for implementing To do App (Task 1 Goal No 5)
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    content = db.Column(db.String(200),nullable = False)
    priority = db.Column(db.Integer, default = 1)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


@app.route('/')                 # main/index route of the app
def index():                    # index function related to index/main route
    tasks = Todo.query.order_by(Todo.priority)
    return render_template('task_master.html', tasks=tasks)



###################################### To do Funciton ################################################

@app.route('/add_todo_task', methods =['GET','POST'] )    # route at which we add the task
def add_todo_task():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form['priority']
        new_task = Todo(content = task_content,priority = task_priority)         # creating to do object
        try:
            db.session.add(new_task)
            db.session.commit()
            tasks = Todo.query.order_by(Todo.priority)
            return render_template('task_master.html', tasks=tasks)
        except:
            return "Task not added in the database"

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        tasks = Todo.query.order_by(Todo.priority)
        return render_template('task_master.html',tasks = tasks)
    except:
        return "OOPS There is a problem while deleting the task"

@app.route('/update_task/<int:id>',methods = ['GET','POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    tasks = Todo.query.order_by(Todo.priority)
    if request.method == 'GET':         # redirect to update task form
        return render_template('update_task.html',task = task,tasks=tasks)
    if request.method == 'POST':
        task.content = request.form['content']
        task.priority= request.form['priority']
        try:
            db.session.commit()
            tasks = Todo.query.order_by(Todo.priority)
            return render_template('task_master.html', tasks=tasks)
        except:
            return "There is an issue while updating the task"

if __name__ == "__main__":
    app.run(debug=True)
