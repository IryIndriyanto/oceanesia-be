from db import db
from enum import Enum


class IssueCategory(Enum):
    TRASH = "trash"
    POLLUTION = "pollution"
    EROSION = "erosion"
    UNSAFE = "unsafe"
    OTHER = "other"


class IssueStatus(Enum):
    OPEN = "withdrawal"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class IssueModel(db.Model):
    __tablename__ = "issue"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    issue_title = db.Column(db.String(255))
    issue_image = db.Column(db.String(255))
    issue_category = db.Column(db.Enum(IssueCategory))
    issue_status = db.Column(db.Enum(IssueStatus))
    issue_description = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now()
    )
