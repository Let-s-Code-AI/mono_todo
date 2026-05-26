"""Epic 4: task history and comments

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-26 12:00:00.000000

"""
from typing import Union

from alembic import op
from sqlalchemy import text


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # Create taskhistory table
    bind.execute(text("""
        CREATE TABLE IF NOT EXISTS taskhistory (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id     INTEGER NOT NULL REFERENCES task(id),
            changed_by_id INTEGER NOT NULL REFERENCES user(id),
            field_name  VARCHAR(100) NOT NULL,
            old_value   VARCHAR(2000),
            new_value   VARCHAR(2000),
            changed_at  DATETIME NOT NULL
        )
    """))
    bind.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_taskhistory_task_id ON taskhistory (task_id)"
    ))
    bind.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_taskhistory_changed_by_id ON taskhistory (changed_by_id)"
    ))

    # Create comment table
    bind.execute(text("""
        CREATE TABLE IF NOT EXISTS comment (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id     INTEGER NOT NULL REFERENCES task(id),
            author_id   INTEGER NOT NULL REFERENCES user(id),
            content     VARCHAR(5000) NOT NULL,
            created_at  DATETIME NOT NULL
        )
    """))
    bind.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_comment_task_id ON comment (task_id)"
    ))
    bind.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_comment_author_id ON comment (author_id)"
    ))


def downgrade() -> None:
    op.drop_index("ix_comment_author_id", table_name="comment")
    op.drop_index("ix_comment_task_id", table_name="comment")
    op.drop_table("comment")
    op.drop_index("ix_taskhistory_changed_by_id", table_name="taskhistory")
    op.drop_index("ix_taskhistory_task_id", table_name="taskhistory")
    op.drop_table("taskhistory")
