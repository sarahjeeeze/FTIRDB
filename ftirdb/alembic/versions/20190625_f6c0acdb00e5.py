"""init

Revision ID: f6c0acdb00e5
Revises: 
Create Date: 2019-06-25 21:04:17.741758

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f6c0acdb00e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('FTIRModel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('magic', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_FTIRModel')),
    sa.UniqueConstraint('name', name=op.f('uq_FTIRModel_name'))
    )
    op.create_table('Graph_experiment',
    sa.Column('spectra_id', sa.Integer(), nullable=False),
    sa.Column('a', sa.Integer(), nullable=False),
    sa.Column('b', sa.Integer(), nullable=False),
    sa.Column('c', sa.Integer(), nullable=False),
    sa.Column('d', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('spectra_id', name=op.f('pk_Graph_experiment'))
    )
    op.create_table('Spectra',
    sa.Column('spectra_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=32), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('spectra_id', name=op.f('pk_Spectra')),
    sa.UniqueConstraint('label', name=op.f('uq_Spectra_label'))
    )
    op.create_table('Spectra_detail',
    sa.Column('spectra_id', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('spectra_id', name=op.f('pk_Spectra_detail')),
    sa.UniqueConstraint('index', name=op.f('uq_Spectra_detail_index'))
    )
    op.create_table('project',
    sa.Column('descriptive_name', sa.String(length=300), nullable=True),
    sa.Column('project_ID', mysql.INTEGER(display_width=4), autoincrement=True, nullable=False),
    sa.Column('related_experiments_ID', sa.String(length=100), nullable=True),
    sa.Column('related_samples_ID', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('project_ID', name=op.f('pk_project')),
    sa.UniqueConstraint('project_ID', name=op.f('uq_project_project_ID'))
    )
    op.create_table('sample',
    sa.Column('sample_ID', mysql.INTEGER(display_width=4), autoincrement=True, nullable=False),
    sa.Column('descriptive_name', sa.String(length=45), nullable=True),
    sa.Column('composition', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('sample_ID', name=op.f('pk_sample')),
    sa.UniqueConstraint('sample_ID', name=op.f('uq_sample_sample_ID'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('role', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('name', name=op.f('uq_users_name'))
    )
    op.create_table('molecules_in_sample',
    sa.Column('molecular_composition_ID', mysql.INTEGER(display_width=4), autoincrement=True, nullable=False),
    sa.Column('descriptive_name', sa.String(length=45), nullable=True),
    sa.Column('molecule_1_name', sa.String(length=45), nullable=True),
    sa.Column('concentration_1', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('molecule_2_name', sa.String(length=45), nullable=True),
    sa.Column('concentration_2', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('molecule_3_name', sa.String(length=45), nullable=True),
    sa.Column('concentration_3', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('molecule_4_name', sa.String(length=45), nullable=True),
    sa.Column('concentration_4', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('sample_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sample_ID'], ['sample.sample_ID'], name=op.f('fk_molecules_in_sample_sample_ID_sample')),
    sa.PrimaryKeyConstraint('molecular_composition_ID', name=op.f('pk_molecules_in_sample')),
    sa.UniqueConstraint('molecular_composition_ID', name=op.f('uq_molecules_in_sample_molecular_composition_ID'))
    )
    op.create_table('state_of_sample',
    sa.Column('state_of_sample_ID', mysql.INTEGER(display_width=4), autoincrement=True, nullable=False),
    sa.Column('state', sa.Enum('gas', 'solid', 'dried film', 'liquid'), nullable=False),
    sa.Column('temperature_degrees', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('pressure_PSI', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('sample_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sample_ID'], ['sample.sample_ID'], name=op.f('fk_state_of_sample_sample_ID_sample')),
    sa.PrimaryKeyConstraint('state_of_sample_ID', name=op.f('pk_state_of_sample')),
    sa.UniqueConstraint('state_of_sample_ID', name=op.f('uq_state_of_sample_state_of_sample_ID'))
    )
    op.create_table('dried_film',
    sa.Column('atmosphere', sa.String(length=45), nullable=True),
    sa.Column('solution_ composition', sa.String(length=45), nullable=True),
    sa.Column('concentration', sa.String(length=45), nullable=True),
    sa.Column('volume', sa.String(length=45), nullable=True),
    sa.Column('area', sa.String(length=45), nullable=True),
    sa.Column('solvent', sa.String(length=45), nullable=True),
    sa.Column('pH', sa.String(length=45), server_default=sa.text("'RANGE(0,14)'"), nullable=True),
    sa.Column('state_of_sample_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['state_of_sample_ID'], ['state_of_sample.state_of_sample_ID'], name=op.f('fk_dried_film_state_of_sample_ID_state_of_sample'))
    )
    op.create_table('gas',
    sa.Column('atmosphere', sa.String(length=45), nullable=True),
    sa.Column('water_vapour', sa.String(length=45), nullable=True),
    sa.Column('state_of_sample_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['state_of_sample_ID'], ['state_of_sample.state_of_sample_ID'], name=op.f('fk_gas_state_of_sample_ID_state_of_sample'))
    )
    op.create_table('liquid',
    sa.Column('solution_composition', sa.String(length=100), nullable=False),
    sa.Column('pH', sa.String(length=45), nullable=True),
    sa.Column('concentration', sa.String(length=45), nullable=True),
    sa.Column('solvent', sa.String(length=45), nullable=True),
    sa.Column('atmosphere', sa.String(length=45), nullable=True),
    sa.Column('sample_ID', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('state_of_sample_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['state_of_sample_ID'], ['state_of_sample.state_of_sample_ID'], name=op.f('fk_liquid_state_of_sample_ID_state_of_sample')),
    sa.PrimaryKeyConstraint('sample_ID', name=op.f('pk_liquid'))
    )
    op.create_table('solid',
    sa.Column('crystal_form', sa.String(length=45), nullable=True),
    sa.Column('chemical_formula', sa.String(length=45), nullable=True),
    sa.Column('state_of_sample_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['state_of_sample_ID'], ['state_of_sample.state_of_sample_ID'], name=op.f('fk_solid_state_of_sample_ID_state_of_sample'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('solid')
    op.drop_table('liquid')
    op.drop_table('gas')
    op.drop_table('dried_film')
    op.drop_table('state_of_sample')
    op.drop_table('molecules_in_sample')
    op.drop_table('users')
    op.drop_table('sample')
    op.drop_table('project')
    op.drop_table('Spectra_detail')
    op.drop_table('Spectra')
    op.drop_table('Graph_experiment')
    op.drop_table('FTIRModel')
    # ### end Alembic commands ###
