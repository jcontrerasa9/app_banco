"""Create accounts table.

Revision ID: e06b6606785f
Revises:
Create Date: 2026-09-03 09:58:39.805174

"""

from alembic import op
import sqlalchemy as sa


revision = "e06b6606785f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("document", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("balance", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("account_number", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_accounts_email"), ["email"], unique=True)
        batch_op.create_index(batch_op.f("ix_accounts_document"), ["document"], unique=True)
        batch_op.create_index(
            batch_op.f("ix_accounts_account_number"), ["account_number"], unique=True
        )


def downgrade():
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_accounts_account_number"))
        batch_op.drop_index(batch_op.f("ix_accounts_document"))
        batch_op.drop_index(batch_op.f("ix_accounts_email"))

    op.drop_table("accounts")