from datetime import datetime
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
        deadline = request.form.get("deadline")
        priority = request.form.get("priority", "medium")

        if content:
            task = Task(
                content=content,
                owner=current_user,
                deadline=datetime.strptime(deadline, "%Y-%m-%d") if deadline else None,
                priority=priority
            )
            db.session.add(task)
            db.session.commit()
            flash("Task added!", "success")
        else:
            flash("Content cannot be empty", "danger")

        return redirect(url_for("todo.list_tasks"))

    # ✅ Filtering logic
    filter_status = request.args.get("filter", "all")
    priority_filter = request.args.get("priority", None)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = Task.query.filter_by(owner=current_user)

    if filter_status == "completed":
        query = query.filter_by(completed=True)
    elif filter_status == "incomplete":
        query = query.filter_by(completed=False)

    if priority_filter:
        query = query.filter_by(priority=priority_filter)

    if start_date and end_date:
        query = query.filter(
            Task.deadline >= datetime.strptime(start_date, "%Y-%m-%d"),
            Task.deadline <= datetime.strptime(end_date, "%Y-%m-%d")
        )

    tasks = query.all()

    return render_template("todos/list.html", tasks=tasks, filter_status=filter_status)

# ✅ UPDATE (toggle completed or edit text)
@bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ensure user owns the task
    if task.owner != current_user:
        flash("You cannot edit this task", "danger")
        return redirect(url_for("todo.list_tasks"))

    if request.method == "POST":
        # Update content
        task.content = request.form.get("content", task.content)

        # Update deadline
        deadline = request.form.get("deadline")
        if deadline:
            try:
                task.deadline = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format", "danger")
        else:
            task.deadline = None

        # Update priority
        task.priority = request.form.get("priority", task.priority)

        # Update completed status
        task.completed = "completed" in request.form

        # Save changes
        db.session.commit()
        flash("Task updated successfully!", "success")
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

# ✅ TOGGLE COMPLETED
@bp.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ensure only owner can toggle
    if task.owner != current_user:
        flash("You cannot modify this task", "danger")
        return redirect(url_for("todo.list_tasks"))

    # Toggle completion
    task.completed = not task.completed
    db.session.commit()

    flash("Task marked as completed!" if task.completed else "Task marked as incomplete!", "success")
    return redirect(url_for("todo.list_tasks"))