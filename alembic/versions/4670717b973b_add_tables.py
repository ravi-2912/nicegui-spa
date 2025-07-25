"""Add tables

Revision ID: 4670717b973b
Revises: 
Create Date: 2025-07-18 00:51:15.602136

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4670717b973b'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brokers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('strategies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suffixes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('symbols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('industry', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('exchange', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('demo', 'live', name='accounttype'), nullable=False),
    sa.Column('platform', sa.Enum('mt5', 'mt4', 'ct5', name='platformtype'), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('currency', sa.Enum('USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD', 'CNY', 'HKD', 'NOK', 'SGD', 'KRW', 'SEK', 'MXN', name='currencytype'), nullable=True),
    sa.Column('starting_balance', sa.Float(), nullable=True),
    sa.Column('current_balance', sa.Float(), nullable=True),
    sa.Column('portable', sa.Boolean(), nullable=False),
    sa.Column('server', sa.String(), nullable=False),
    sa.Column('broker_id', sa.Integer(), nullable=True),
    sa.Column('archived', sa.Boolean(), nullable=False),
    sa.Column('is_valid', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['broker_id'], ['brokers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('instruments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('symbol_id', sa.Integer(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('suffix_id', sa.Integer(), nullable=True),
    sa.Column('lot_size', sa.Float(), nullable=True),
    sa.Column('leverage', sa.Integer(), nullable=True),
    sa.Column('min_volume', sa.Float(), nullable=True),
    sa.Column('max_volume', sa.Float(), nullable=True),
    sa.Column('step_volume', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['suffix_id'], ['suffixes.id'], ),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ticker', 'symbol_id', 'account_id', name='unique_instrument')
    )
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trade_id', sa.String(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('symbol_id', sa.String(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('strategy_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('active', 'pending', 'closed', name='tradestatustype'), nullable=False),
    sa.Column('risk', sa.Float(), nullable=False),
    sa.Column('direction', sa.Enum('long', 'short', name='directiontype'), nullable=False),
    sa.Column('order_type', sa.Enum('market', 'limit', 'stop', name='ordertype'), nullable=False),
    sa.Column('lots', sa.Float(), nullable=False),
    sa.Column('units', sa.Integer(), nullable=False),
    sa.Column('entry_price', sa.Float(), nullable=False),
    sa.Column('stop_loss_pips', sa.Float(), nullable=True),
    sa.Column('take_profit_pips', sa.Float(), nullable=True),
    sa.Column('stop_loss_price', sa.Float(), nullable=True),
    sa.Column('take_profit_price', sa.Float(), nullable=True),
    sa.Column('open_time', sa.DateTime(), nullable=False),
    sa.Column('exit_time', sa.DateTime(), nullable=True),
    sa.Column('exit_price', sa.Float(), nullable=True),
    sa.Column('probability', sa.Enum('very_high', 'high', 'medium', 'low', name='tradesuccessprobabilitytype'), nullable=False),
    sa.Column('mindstate', sa.Enum('fresh', 'energetic', 'hyper', 'lazy', 'tired', 'sleepy', 'exhausted', 'sad', 'gloomy', 'anxious', 'fearful', 'angry', 'frustrated', 'panicked', 'depressed', 'regretful', 'disappointed', 'vengeful', 'happy', 'calm', 'confident', 'excited', 'hopeful', 'euphoric', 'satisfied', 'grateful', 'focused', 'distracted', 'confused', 'overwhelmed', 'mindful', 'impulsive', 'rational', 'reactive', 'indifferent', 'zoned_out', 'tunnel_vision', 'flow', 'normal', 'active', 'neutral', 'aggressive', 'defensive', 'cautious', 'reckless', 'overconfident', 'disciplined', 'emotional', 'robotic', 'burnt_out', 'patient', 'bored', 'curious', 'stressed', 'under_pressure', 'relief', name='tradingmindstate'), nullable=False),
    sa.Column('_duration_seconds', sa.Integer(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('reward_risk', sa.Float(), nullable=True),
    sa.Column('exit_reason', sa.Enum('take_profit', 'stop_loss', 'cancelled', 'manual', name='exitreasontype'), nullable=True),
    sa.Column('exit_reason_details', sa.String(), nullable=True),
    sa.Column('actual_pnl', sa.Float(), nullable=True),
    sa.Column('actual_reward_risk', sa.Float(), nullable=True),
    sa.Column('starting_balance', sa.Float(), nullable=True),
    sa.Column('ending_balance', sa.Float(), nullable=True),
    sa.Column('validated_from_backtest', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id'], ),
    sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id'], ),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trade_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trade_id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trade_notes')
    op.drop_table('trades')
    op.drop_table('instruments')
    op.drop_table('accounts')
    op.drop_table('symbols')
    op.drop_table('suffixes')
    op.drop_table('strategies')
    op.drop_table('brokers')
    # ### end Alembic commands ###
