"""Projects: project and projectmember tables, task.project_id

Revision ID: 032f9cfa00ce
Revises: c3d4e5f6a7b8
Create Date: 2026-10-19 15:24:47.948042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '032f9cfa00ce'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

