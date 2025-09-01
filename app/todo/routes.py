from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Task
from . import bp

# ✅ READ + CREATE
@bp.route("/", methods=["GET", "POST"])
@login_required
def list_tasks():
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            task = Task(content=content, owner=current_user)
            db.session.add(task)
            db.session.commit()
            flash("Task added!", "success")
        else:
            flash("Content cannot be empty", "danger")
        return redirect(url_for("todo.list_tasks"))

    # ✅ Filtering
    filter_status = request.args.get("filter", "all")
    if filter_status == "completed":
        tasks = Task.query.filter_by(owner=current_user, completed=True).all()
    elif filter_status == "incomplete":
        tasks = Task.query.filter_by(owner=current_user, completed=False).all()
    else:
        tasks = current_user.tasks

    return render_template("todos/list.html", tasks=tasks, filter_status=filter_status)

# ✅ UPDATE (toggle completed or edit text)
@bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash("You cannot edit this task", "danger")
        return redirect(url_for("todo.list_tasks"))

    if request.method == "POST":
        task.content = request.form.get("content", task.content)
        task.completed = "completed" in request.form
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("todo.list_tasks"))

    return render_template("todos/edit.html", task=task)

# ✅ DELETE
@bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash("You cannot delete this task", "danger")
        return redirect(url_for("todo.list_tasks"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "danger")   # 👈 now marked as danger
    return redirect(url_for("todo.list_tasks"))