"""Epic 4: task history and comments

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-26 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # Create taskhistory table
    bind.execute(text("""
        CREATE TABLE IF NOT EXISTS taskhistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL REFERENCES task(id),
            user_id INTEGER NOT NULL REFERENCES user(id),
            field_name VARCHAR(100) NOT NULL,
            old_value VARCHAR(1000),
            new_value VARCHAR(1000),
            changed_at DATETIME NOT NULL
        )
    """))
    bind.execute(text("CREATE INDEX IF NOT EXISTS ix_taskhistory_task_id ON taskhistory (task_id)"))

    # Create taskcomment table
    bind.execute(text("""
        CREATE TABLE IF NOT EXISTS taskcomment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL REFERENCES task(id),
            user_id INTEGER NOT NULL REFERENCES user(id),
            content VARCHAR(2000) NOT NULL,
            created_at DATETIME NOT NULL
        )
    """))
    bind.execute(text("CREATE INDEX IF NOT EXISTS ix_taskcomment_task_id ON taskcomment (task_id)"))


def downgrade() -> None:
    op.drop_index("ix_taskcomment_task_id", table_name="taskcomment")
    op.drop_table("taskcomment")
    op.drop_index("ix_taskhistory_task_id", table_name="taskhistory")
    op.drop_table("taskhistory")
