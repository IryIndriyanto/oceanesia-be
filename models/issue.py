from db import db


class IssueModel(db.Model):
    __tablename__ = "issue"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    issue_title = db.Column(db.String(255))
    issue_image = db.Column(db.String(255))
    issue_category = db.Column(db.Enum("Category1", "Category2", "Category3"))
    issue_status = db.Column(db.Enum("Open", "In Progress", "Closed"))
    issue_description = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now()
    )
