"""empty message

Revision ID: e4a7b3a356b8
Revises: 
Create Date: 2021-04-20 13:57:51.164490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4a7b3a356b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('hr_review_statuses',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('positions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ratings',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=25), nullable=False),
    sa.Column('value', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('value')
    )
    op.create_table('review_periods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('statuses',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('fullname', sa.VARCHAR(length=255), nullable=False),
    sa.Column('chat_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('boss_id', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.SmallInteger(), nullable=False),
    sa.Column('position_id', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['boss_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('coworker_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('hr_status_id', sa.SmallInteger(), nullable=True),
    sa.Column('coworker_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coworker_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['hr_status_id'], ['hr_review_statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('forms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('review_period_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['review_period_id'], ['review_periods.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('boss_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('boss_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['boss_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coworker_advices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('todo', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('not_todo', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('hr_comment', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('coworker_review_id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coworker_review_id'], ['coworker_reviews.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('duties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('form_id')
    )
    op.create_table('fails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('description', sa.VARCHAR(length=2000), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coworker_project_ratings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('hr_comment', sa.VARCHAR(length=1000), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('rating_id', sa.Integer(), nullable=True),
    sa.Column('coworker_review_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coworker_review_id'], ['coworker_reviews.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['rating_id'], ['ratings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coworker_project_ratings')
    op.drop_table('projects')
    op.drop_table('fails')
    op.drop_table('duties')
    op.drop_table('coworker_advices')
    op.drop_table('boss_reviews')
    op.drop_table('achievements')
    op.drop_table('forms')
    op.drop_table('coworker_reviews')
    op.drop_table('users')
    op.drop_table('statuses')
    op.drop_table('roles')
    op.drop_table('review_periods')
    op.drop_table('ratings')
    op.drop_table('positions')
    op.drop_table('hr_review_statuses')
    op.drop_table('departments')
    # ### end Alembic commands ###
