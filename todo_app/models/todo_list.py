from odoo import models, fields, api


class ToDoList(models.Model):
    _name = "todo.list"
    _description = "Helps you organize your tasks"
    _order = "is_complete DESC, deadline"

    title = fields.Char(
        string="Title",
        require=True,
    )
    name = fields.Char(
        string="Reference",
        readonly=True,
        default="New",
    )
    description = fields.Text(string="Description")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submit", "Submitted"),
            ("open", "In Progress"),
            ("close", "Closed"),
        ],
        default="draft",
    )
    type = fields.Selection(
        selection=[
            ("bug", "Bug"),
            ("feat", "Feature"),
            ("imp", "Improvement"),
            ("other", "Other"),
        ],
        default="other",
    )
    deadline = fields.Date(string="Deadline")
    product_owner_id = fields.Many2one(
        string="Requested By",
        comodel_name="person.in.charge",
        require=True,
        domain="[('type', '=', 'pmo')]",
        help="Helps you keep track on who is assigning the task."
    )
    developer_id = fields.Many2one(
        string="Assigned To",
        comodel_name="person.in.charge",
        domain="[('type', '=', 'dev')]",
        help="Help you keep track on who is responsible for the task."
    )
    stakeholder_ids = fields.Many2many(
        string="Belongs To",
        comodel_name="stakeholder",
        column1="todo_list_id",
        column2="stakeholder_id",
        relation="todo_list_stakeholder_rel",
        help="Helps you keep track on which Clients to deploy to on the tasks."
    )
    is_complete = fields.Boolean(
        string="Mark as Complete",
        default=False,
    )

    @api.model
    def create(self, vals):
        vals["name"] = self._get_sequence(todo_list_type=vals["type"])
        return super(ToDoList, self).create(vals)

    def _get_sequence(self, todo_list_type):
        """
        Get Sequence based on the given type

        :param str todo_list_type: To-Do List Type
        :return: Next Sequence
        """
        if not todo_list_type:
            raise ValueError("Invalid Todo List Type.")

        sequence_code = {
            "bug": "todo.list.bug",
            "feat": "todo.list.feat",
            "imp": "todo.list.imp",
            "other": "todo.list.other",
        }

        if todo_list_type not in sequence_code.keys():
            raise ValueError("Invalid Todo List Type.")

        return self.env["ir.sequence"].next_by_code(sequence_code=sequence_code.get(todo_list_type))

    def reset_to_draft(self):
        for record in self:
            record.write({
                "state": "draft",
                "is_complete": False,
            })

    def submit(self):
        for record in self:
            record.write({"state": "submit"})

    def set_to_progress(self):
        for record in self:
            record.write({"state": "open"})

    def mark_as_done(self):
        for record in self:
            record.write({
                "state": "close",
                "is_complete": True,
            })
