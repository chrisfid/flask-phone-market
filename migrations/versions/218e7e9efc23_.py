"""empty message

Revision ID: 218e7e9efc23
Revises: 7e8546448edc
Create Date: 2021-05-21 22:55:16.149773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '218e7e9efc23'
down_revision = '7e8546448edc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'image_file',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'image_file',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###
