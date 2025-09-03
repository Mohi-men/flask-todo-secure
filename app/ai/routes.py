from flask import request, jsonify
from flask_login import login_required, current_user
from ..models import Task
from . import bp
from .rag import build_index, query_index
from datetime import datetime, timedelta

@bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    query = data.get("query", "").lower()

    # Fetch tasks
    tasks = Task.query.filter_by(owner=current_user).all()
    if not tasks:
        return jsonify({"answer": "You don’t have any tasks yet."}), 200

    # Filtering (priority/completion/date — simplified from earlier code)
    filtered_tasks = tasks
    if "completed" in query:
        filtered_tasks = [t for t in filtered_tasks if t.completed]
    elif "incomplete" in query or "pending" in query:
        filtered_tasks = [t for t in filtered_tasks if not t.completed]

    if "low priority" in query:
        filtered_tasks = [t for t in filtered_tasks if t.priority == "low"]
    elif "medium priority" in query:
        filtered_tasks = [t for t in filtered_tasks if t.priority == "medium"]
    elif "high priority" in query:
        filtered_tasks = [t for t in filtered_tasks if t.priority == "high"]

    today = datetime.today().date()
    if "today" in query:
        filtered_tasks = [t for t in filtered_tasks if t.deadline and t.deadline.date() == today]
    elif "tomorrow" in query:
        tomorrow = today + timedelta(days=1)
        filtered_tasks = [t for t in filtered_tasks if t.deadline and t.deadline.date() == tomorrow]
    elif "this week" in query:
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        filtered_tasks = [t for t in filtered_tasks if t.deadline and start <= t.deadline.date() <= end]
    elif "next week" in query:
        start = today - timedelta(days=today.weekday()) + timedelta(weeks=1)
        end = start + timedelta(days=6)
        filtered_tasks = [t for t in filtered_tasks if t.deadline and start <= t.deadline.date() <= end]
    elif "this month" in query:
        start = today.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = start.replace(month=start.month + 1, day=1) - timedelta(days=1)
        filtered_tasks = [t for t in filtered_tasks if t.deadline and start <= t.deadline.date() <= end]

    # Format as JSON
    result = []
    for t in filtered_tasks:
        result.append({
            "content": t.content,
            "priority": t.priority,
            "deadline": t.deadline.strftime("%Y-%m-%d") if t.deadline else None,
            "completed": t.completed
        })

    return jsonify({
        "answer": f"Found {len(result)} task(s) for your query.",
        "tasks": result
    })