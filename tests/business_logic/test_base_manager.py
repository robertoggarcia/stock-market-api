from freezegun import freeze_time
from sqlalchemy.orm import Session

from app.business_logic import constans
from app.business_logic.base_manager import BaseManager


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_open_market(db: Session, account):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert base_manager._is_market_open()


@freeze_time("2023-03-27 19:00:00-06:00")
def test_base_manager_open_market_false(db: Session, account):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._is_market_open()


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_valid_op(db: Session, account, order_schema):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert base_manager._can_be_processed(order=order_schema)
    assert not base_manager.errors


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_invalid_op(db: Session, account, order_schema):
    order_schema.operation = "test"
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.INVALID_OPERATION]


@freeze_time("2023-03-27 19:00:00-06:00")
def test_base_manager_can_be_processed_close_market(db: Session, account, order_schema):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.CLOSED_MARKET]