from flask import Flask, render_template, request, redirect  # add
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # add
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # add
db = SQLAlchemy(app)  # add

# add


class Task(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(80), nullable=False)
   created_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.now)

   def __repr__(self):
       return f'Todo : {self.name}'


@app.route("/", methods=['POST', 'GET'])
def home():
   if request.method == "POST": # add
       name = request.form['name']
       new_task = Task(name=name)
       db.session.add(new_task)
       db.session.commit()
       return redirect('/')
   else:
       tasks = Task.query.order_by(Task.created_at).all()  # add
   return render_template("home.html", tasks=tasks)  # add

# update task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
   task = Task.query.get_or_404(id)

   if request.method == 'POST':
       task.name = request.form['name']

       try:
           db.session.commit()
           return redirect('/')
       except:
           return "There was a problem updating data."

   else:
       title = "Update Task"
       return render_template('update.html', title=title, task=task)
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try: 
        db.session.delete(task)
        db.sess.commit()
        return redirect('/')
    except Exception:
        return "There was a problem Deleting Data"

if __name__ == "__main__":
   app.run(debug=True)