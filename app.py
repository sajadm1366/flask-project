from email.policy import default
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
       task_content = request.form['content']
       new_task = Tasks(content=task_content)
       db.session.add(new_task)
       db.session.commit()
       return redirect(url_for('home'))
    else:
        tasks = Tasks.query.all()
        return render_template("home.html", tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    taks_to_delete = Tasks.query.get_or_404(id) 
    db.session.delete(taks_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task  = Tasks.query.get_or_404(id)
    if request.method == 'POST':
       task.content = request.form['content']
       db.session.commit()
       return redirect('/')
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)