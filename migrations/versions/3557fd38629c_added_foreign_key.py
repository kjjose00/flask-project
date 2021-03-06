"""added foreign key

Revision ID: 3557fd38629c
Revises: 48df50fff290
Create Date: 2021-09-26 13:38:32.912097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3557fd38629c'
down_revision = '48df50fff290'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('poster_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['poster_id'], ['id'])
    op.drop_column('posts', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'poster_id')
    # ### end Alembic commands ###
