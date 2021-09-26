"""empty message

Revision ID: 786f6c92c039
Revises: 7a33d6eccdb5
Create Date: 2021-09-26 04:02:27.361790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '786f6c92c039'
down_revision = '7a33d6eccdb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'movies', ['title'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movies', type_='unique')
    op.alter_column('movies', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
