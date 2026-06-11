from flask import Blueprint, flash, redirect, render_template, request, url_for

from helpdesk_lite.services.comment_service import CommentService
from helpdesk_lite.services.issue_service import IssueService
from helpdesk_lite.services.user_service import UserService


issues_bp = Blueprint("issues", __name__, url_prefix="/issues")
issue_service = IssueService()
comment_service = CommentService()
user_service = UserService()


@issues_bp.get("/")
def list_issues():
    search = request.args.get("q", "")
    status = request.args.get("status", "")
    issues = issue_service.list_issues(search_term=search or None, status=status)
    rows = [issue_service.summarize_issue_for_list(issue) for issue in issues]
    return render_template(
        "issues/list.html", issues=issues, rows=rows, search=search, status=status
    )


@issues_bp.route("/new", methods=["GET", "POST"])
def create_issue():
    if request.method == "POST":
        issue, errors = issue_service.create_issue(
            request.form.get("title", ""),
            request.form.get("description", ""),
            request.form.get("reporter_name", ""),
            request.form.get("priority", "medium"),
        )
        if not errors:
            flash("Issue created.", "success")
            return redirect(url_for("issues.view_issue", issue_id=issue.id))

        for error in errors:
            flash(error, "error")

    return render_template("issues/new.html")


@issues_bp.get("/<int:issue_id>")
def view_issue(issue_id):
    issue = issue_service.get_issue(issue_id)
    if not issue:
        flash("Issue not found.", "error")
        return redirect(url_for("issues.list_issues"))

    comments = comment_service.list_for_issue(issue_id)
    users = user_service.list_users()
    return render_template(
        "issues/detail.html", issue=issue, comments=comments, users=users
    )


@issues_bp.route("/<int:issue_id>/edit", methods=["GET", "POST"])
def edit_issue(issue_id):
    issue = issue_service.get_issue(issue_id)
    if not issue:
        flash("Issue not found.", "error")
        return redirect(url_for("issues.list_issues"))

    if request.method == "POST":
        updated, errors = issue_service.edit_issue(
            issue_id,
            request.form.get("title", ""),
            request.form.get("description", ""),
            request.form.get("priority", "medium"),
        )
        if not errors:
            flash("Issue updated.", "success")
            return redirect(url_for("issues.view_issue", issue_id=updated.id))

        for error in errors:
            flash(error, "error")

    return render_template("issues/edit.html", issue=issue)


@issues_bp.post("/<int:issue_id>/close")
def close_issue(issue_id):
    issue, errors = issue_service.close_issue(issue_id)
    for error in errors:
        flash(error, "error")
    if not errors:
        flash("Issue closed.", "success")
    return redirect(url_for("issues.view_issue", issue_id=issue_id))


@issues_bp.post("/<int:issue_id>/reopen")
def reopen_issue(issue_id):
    issue, errors = issue_service.reopen_issue(issue_id)
    for error in errors:
        flash(error, "error")
    if not errors:
        flash("Issue reopened.", "success")
    return redirect(url_for("issues.view_issue", issue_id=issue_id))


@issues_bp.post("/<int:issue_id>/assign")
def assign_issue(issue_id):
    issue = issue_service.get_issue(issue_id)
    if issue and issue.status.upper() == "CLOSED":
        flash("Closed issues cannot be assigned.", "error")
        return redirect(url_for("issues.view_issue", issue_id=issue_id))

    updated, errors = issue_service.assign_issue(issue_id, request.form.get("user_id"))
    for error in errors:
        flash(error, "error")
    if not errors:
        flash("Assignment updated.", "success")
    return redirect(url_for("issues.view_issue", issue_id=issue_id))


@issues_bp.post("/<int:issue_id>/comments")
def add_comment(issue_id):
    comment, errors = comment_service.add_comment(
        issue_id,
        request.form.get("author_name", ""),
        request.form.get("body", ""),
    )
    for error in errors:
        flash(error, "error")
    if not errors:
        flash("Comment added.", "success")
    return redirect(url_for("issues.view_issue", issue_id=issue_id))
