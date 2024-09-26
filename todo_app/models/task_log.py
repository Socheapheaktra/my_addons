from odoo import models, fields


class TaskLog(models.Model):
    _name = "task.log"

    name = fields.Text(
        string="Description",
        require=True,
    )
    todo_id = fields.Many2one(
        string="Task",
        comodel_name="todo.list",
        require=True,
        readonly=True,
    )
