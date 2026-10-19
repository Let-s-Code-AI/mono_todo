"""Task change history table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-10-19 09:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Dev/test startup runs create_all, which may already have built this table (and index).
    if "taskhistory" in sa.inspect(op.get_bind()).get_table_names():
        return
    op.create_table(
        "taskhistory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("changed_by_id", sa.Integer(), nullable=True),
        sa.Column("field", sa.String(length=50), nullable=False),
        sa.Column("old_value", sa.String(), nullable=True),
        sa.Column("new_value", sa.String(), nullable=True),
        sa.Column("changed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["changed_by_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["task.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_taskhistory_task_id"), "taskhistory", ["task_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_taskhistory_task_id"), table_name="taskhistory")
    op.drop_table("taskhistory")
