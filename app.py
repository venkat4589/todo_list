from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_app"
app.config["SECRET_KEY"] = "3f9bd8c7f23950c63c4d5f343facdf00e9b8958e6efc31a077f6cbdf8a1eadb6"  # Replace with your generated key

mongo = PyMongo(app)

@app.route('/')
def index():
    tasks = mongo.db.tasks.find()
    tasks = [{**task, '_id': str(task['_id'])} for task in tasks]
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        mongo.db.tasks.insert_one({'name': task_name, 'description': task_description})
        flash('Task Added Successfully')
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'name': task_name, 'description': task_description}})
        flash('Task Updated Successfully')
        return redirect(url_for('index'))
    task['_id'] = str(task['_id'])
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    flash('Task Deleted Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
