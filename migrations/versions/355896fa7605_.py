"""empty message

Revision ID: 355896fa7605
Revises: d5e5a1f6669b
Create Date: 2023-08-24 14:39:31.163624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '355896fa7605'
down_revision = 'd5e5a1f6669b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('pokemon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pokemon_id'], ['caught__pokemon.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    # ### end Alembic commands ###
