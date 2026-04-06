from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save tasks to file
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def home():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()
    task_text = request.form.get("task")

    if task_text.strip():
        tasks.append({"id": len(tasks) + 1, "task": task_text})
        save_tasks(tasks)

    return redirect(url_for("home"))

@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    tasks = load_tasks()
    new_text = request.form.get("task")

    for t in tasks:
        if t["id"] == task_id:
            t["task"] = new_text
            break

    save_tasks(tasks)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]

    # reassign IDs
    for i, t in enumerate(tasks, start=1):
        t["id"] = i

    save_tasks(tasks)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)