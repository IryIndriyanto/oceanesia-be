from marshmallow import Schema, fields


class IssueSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    issue_title = fields.String(required=True, validate=lambda s: len(s) <= 255)
    issue_image = fields.String(required=True, validate=lambda s: len(s) <= 255)
    issue_category = fields.String(
        required=True, validate=lambda s: s in ["Category1", "Category2", "Category3"]
    )
    issue_status = fields.String(
        required=True, validate=lambda s: s in ["Open", "In Progress", "Closed"]
    )
    issue_description = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
