"""empty message

Revision ID: 4050b9b0a148
Revises: c71927fc5fab
Create Date: 2020-01-07 19:59:36.837752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4050b9b0a148'
down_revision = 'c71927fc5fab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('list_task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('list_task_id', sa.Integer(), nullable=False),
    sa.Column('todo', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['list_task_id'], ['list_task.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('list_task')
    # ### end Alembic commands ###
