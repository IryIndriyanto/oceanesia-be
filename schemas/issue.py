from marshmallow import Schema, fields


class IssueSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    location_id = fields.Integer(required=True)
    issue_title = fields.String(required=True)
    issue_image = fields.String(required=True)
    issue_category = fields.String(required=True)
    issue_status = fields.String(required=True)
    issue_description = fields.String(required=True)


class EditIssueStatusSchema(Schema):
    issue_status = fields.String(required=True)
