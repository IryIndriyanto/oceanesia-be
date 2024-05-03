from db import db
from flask import jsonify
from flask_smorest import Blueprint, abort
from schemas.issue import IssueSchema
from models.issue import IssueModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


blp = Blueprint("issues", "issues", description="data of issues", url_prefix="/issues")


@blp.route("/", methods=["GET"])
@blp.response(200, IssueSchema(many=True))
def get_all_issues():
    return IssueModel.query.all()

@blp.route("/", methods=["POST"])
@blp.arguments(IssueSchema)
@blp.response(200)
def create_issue(issue_data):
    issue = IssueModel(**issue_data)

    try:
        db.session.add(issue)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_info = str(e.orig)
        return jsonify({"message": f"IntegrityError: {error_info}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        error_info = str(e)
        return jsonify({"message": f"SQLAlchemyError: {error_info}"}), 500


@blp.route("/<int:issue_id>", methods=["GET"])
@blp.response(200, IssueSchema)
def get_issue_by_id(issue_id):
    issue = IssueModel.query.get(issue_id)
    if issue:
        return issue
    else:
        abort(404, message="Issue not found")


@blp.route("/<int:issue_id>", methods=["DELETE"])
@blp.response(204)
def delete_issue(issue_id):
    issue = IssueModel.query.get(issue_id)
    if issue:
        db.session.delete(issue)
        db.session.commit()
        return None
    else:
        return jsonify(message="Issue not found"), 404


@blp.route("/<int:issue_id>", methods=["PUT"])
@blp.arguments(IssueSchema)
@blp.response(200, IssueSchema)
def edit_issue(issue_data, issue_id):
    issue = IssueModel.query.get(issue_id)
    if issue:
        issue.title = issue_data["title"]
        issue.description = issue_data["description"]
        db.session.commit()
        return issue
    else:
        return jsonify(message="Issue not found"), 404
