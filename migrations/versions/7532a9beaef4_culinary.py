"""'culinary'

Revision ID: 7532a9beaef4
Revises: 
Create Date: 2024-08-26 17:40:46.869042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7532a9beaef4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_recipes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recipes_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipes_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'recipes_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_recipes')
    op.drop_table('user')
    op.drop_table('recipes')
    # ### end Alembic commands ###
