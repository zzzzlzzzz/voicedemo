"""Initial version

Revision ID: a5a1ad7d7939
Revises: 
Create Date: 2019-10-08 16:21:18.286979+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5a1ad7d7939'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entity',
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('entity_id')
    )
    op.create_table('email',
    sa.Column('email_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('email_id')
    )
    op.create_table('phone',
    sa.Column('phone_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=16), nullable=False),
    sa.Column('is_mobile', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('phone_id')
    )
    op.create_table('service',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('is_main', sa.Boolean(), nullable=False),
    sa.Column('available_from', sa.DateTime(), nullable=False),
    sa.Column('available_to', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('service_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service')
    op.drop_table('phone')
    op.drop_table('email')
    op.drop_table('entity')
    # ### end Alembic commands ###