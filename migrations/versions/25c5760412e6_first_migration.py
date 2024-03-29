"""First migration

Revision ID: 25c5760412e6
Revises: 
Create Date: 2019-06-29 01:37:56.302669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25c5760412e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('base_score', sa.Integer(), nullable=True),
    sa.Column('completed_challenges', sa.Integer(), nullable=True),
    sa.Column('base_completed_challenges', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('_codewars_username', sa.String(length=120), nullable=True),
    sa.Column('_skills', sa.String(length=900), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('skills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('probability', sa.Float(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('forwared_to_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.ForeignKeyConstraint(['forwared_to_id'], ['participants.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['participants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    op.drop_table('skills')
    op.drop_table('participants')
    # ### end Alembic commands ###
