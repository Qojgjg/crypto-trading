from abc import ABC, abstractmethod

import model


class AbstractRepository(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def add_trade(self, trade):
        raise NotImplementedError

    @abstractmethod
    def get_trade(self, id):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def update_trade_on_oco_order_creation(self, id, oco_stop_exchange_id,
                                           oco_limit_exchange_id):
        raise NotImplementedError

    @abstractmethod
    def update_trade_on_exit_position(self, id, fiat_result_no_fees, status,
                                      crypto_quantity_exit, exit_fee_fiat,
                                      exit_date):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def add_trade(self, trade):
        self.session.add(trade)

    def get_trade(self, id):
        return self.session.query(model.Trade).filter_by(id=id).one()

    def commit(self):
        self.session.commit()

    def update_trade_on_oco_order_creation(self, id, oco_stop_exchange_id,
                                           oco_limit_exchange_id):
        trade = self.get_trade(id)
        trade.oco_stop_exchange_id = oco_stop_exchange_id
        trade.oco_limit_exchange_id = oco_limit_exchange_id
        self.commit()

    def update_trade_on_exit_position(self, id, fiat_result_no_fees, status,
                                      crypto_quantity_exit, exit_fee_fiat,
                                      exit_date):
        trade = self.get_trade(id)
        trade.fiat_result_no_fees = fiat_result_no_fees
        trade.status = status
        trade.crypto_quantity_exit = crypto_quantity_exit
        trade.exit_fee_fiat = exit_fee_fiat
        trade.exit_date = exit_date
        self.commit()
