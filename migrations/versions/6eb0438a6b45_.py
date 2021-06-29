"""add post table

Revision ID: 6eb0438a6b45
Revises: 
Create Date: 2021-05-23 10:37:32.177501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eb0438a6b45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('time_created', sa.DateTime(timezone=True),
                              server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
