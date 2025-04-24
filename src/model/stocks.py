from sqlalchemy import Boolean, Column, DateTime, Index, Integer, Numeric, String, BigInteger, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "mysql+pymysql://root:123456@localhost:3306/stock"
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    symbol = Column(String(10), nullable=False, index=True, comment="股票代码")
    net_profit_cagr = Column(Numeric(precision=20, scale=4), nullable=True, comment="净利润复合增长率")
    north_net_inflow = Column(Numeric(precision=20, scale=4), nullable=True, comment="北向资金净流入")
    ps = Column(Numeric(precision=20, scale=4), nullable=True, comment="市销率")
    type = Column(Integer, nullable=False, comment="类型")
    percent = Column(Numeric(precision=20, scale=4), nullable=True, comment="涨跌幅")
    has_follow = Column(Boolean, nullable=False, comment="是否关注")
    tick_size = Column(Numeric(precision=20, scale=4), nullable=False, comment="最小变动单位")
    pb_ttm = Column(Numeric(precision=20, scale=4), nullable=True, comment="市净率TTM")
    float_shares = Column(BigInteger, nullable=False, comment="流通股数")
    current = Column(Numeric(precision=20, scale=4), nullable=False, comment="当前价格")
    amplitude = Column(Numeric(precision=20, scale=4), nullable=True, comment="振幅")
    pcf = Column(Numeric(precision=20, scale=4), nullable=True, comment="市现率")
    current_year_percent = Column(Numeric(precision=20, scale=4), nullable=True, comment="年初至今涨跌幅")
    float_market_capital = Column(Numeric(precision=20, scale=4), nullable=True, comment="流通市值")
    north_net_inflow_time = Column(DateTime, nullable=True, comment="北向资金净流入时间")
    market_capital = Column(Numeric(precision=20, scale=4), nullable=True, comment="市值")
    dividend_yield = Column(Numeric(precision=20, scale=4), nullable=True, comment="股息率")
    lot_size = Column(Integer, nullable=False, comment="每手股数")
    roe_ttm = Column(Numeric(precision=20, scale=4), nullable=True, comment="净资产收益率TTM")
    total_percent = Column(Numeric(precision=20, scale=4), nullable=True, comment="总涨跌幅")
    percent5m = Column(Numeric(precision=20, scale=4), nullable=True, comment="5分钟涨跌幅")
    income_cagr = Column(Numeric(precision=20, scale=4), nullable=True, comment="收入复合增长率")
    amount = Column(Numeric(precision=20, scale=4), nullable=True, comment="成交额")
    chg = Column(Numeric(precision=20, scale=4), nullable=True, comment="涨跌额")
    issue_date_ts = Column(BigInteger, nullable=False, comment="发行日期时间戳")
    eps = Column(Numeric(precision=20, scale=4), nullable=True, comment="每股收益")
    main_net_inflows = Column(Numeric(precision=20, scale=4), nullable=True, comment="主力净流入")
    volume = Column(BigInteger, nullable=True, comment="成交量")
    volume_ratio = Column(Numeric(precision=20, scale=4), nullable=True, comment="量比")
    pb = Column(Numeric(precision=20, scale=4), nullable=True, comment="市净率")
    followers = Column(Integer, nullable=False, comment="关注人数")
    turnover_rate = Column(Numeric(precision=20, scale=4), nullable=True, comment="换手率")
    mapping_quote_current = Column(Numeric(precision=20, scale=4), nullable=True, comment="映射报价当前")
    first_percent = Column(Numeric(precision=20, scale=4), nullable=True, comment="首日涨跌幅")
    name = Column(String(20), nullable=False, index=True, comment="股票名称")
    pe_ttm = Column(Numeric(precision=20, scale=4), nullable=True, comment="市盈率TTM")
    dual_counter_mapping_symbol = Column(String(10), nullable=True, comment="双柜台映射代码")
    total_shares = Column(BigInteger, nullable=False, comment="总股本")
    limitup_days = Column(Integer, nullable=False, comment="涨停天数")

    __table_args__ = (
        Index("ix_stock_symbol", symbol),
        Index("ix_stock_name", name),
    )
    


class StockDay(Base):
    __tablename__ = 'stock_day'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    symbol = Column(String(10), nullable=False, comment="股票代码")
    name = Column(String(20), nullable=False, comment="股票名称")

    datetime = Column(DateTime, nullable=True, comment="日期时间")
    timestamp = Column(BigInteger, nullable=True, comment="时间戳")
    volume = Column(BigInteger, nullable=True, comment="成交量")
    open = Column(Numeric(precision=20, scale=4), nullable=True, comment="开盘价")
    high = Column(Numeric(precision=20, scale=4), nullable=True, comment="最高价")
    low = Column(Numeric(precision=20, scale=4), nullable=True, comment="最低价")
    close = Column(Numeric(precision=20, scale=4), nullable=True, comment="收盘价")
    chg = Column(Numeric(precision=20, scale=4), nullable=True, comment="涨跌额")
    percent = Column(Numeric(precision=20, scale=4), nullable=True, comment="涨跌幅")
    turnoverrate = Column(Numeric(precision=20, scale=4), nullable=True, comment="换手率")
    amount = Column(Numeric(precision=20, scale=4), nullable=True, comment="成交额")
    volume_post = Column(Numeric(precision=20, scale=4), nullable=True, comment="成交量")
    amount_post = Column(Numeric(precision=20, scale=4), nullable=True, comment="成交额")
    pe = Column(Numeric(precision=20, scale=4), nullable=True, comment="市盈率")
    pb = Column(Numeric(precision=20, scale=4), nullable=True, comment="市净率")
    ps = Column(Numeric(precision=20, scale=4), nullable=True, comment="市销率")
    pcf = Column(Numeric(precision=20, scale=4), nullable=True, comment="市现率")
    market_capital = Column(Numeric(precision=20, scale=4), nullable=True, comment="市值")
    balance = Column(Numeric(precision=20, scale=4), nullable=True, comment="净资产")
    hold_volume_cn = Column(Numeric(precision=20, scale=4), nullable=True, comment="持筹量")
    hold_ratio_cn = Column(Numeric(precision=20, scale=4), nullable=True, comment="持筹比例")
    net_volume_cn = Column(Numeric(precision=20, scale=4), nullable=True, comment="净量")
    hold_volume_hk = Column(Numeric(precision=20, scale=4), nullable=True, comment="持筹量HK")
    hold_ratio_hk = Column(Numeric(precision=20, scale=4), nullable=True, comment="持筹比例HK")
    net_volume_hk = Column(Numeric(precision=20, scale=4), nullable=True, comment="净量HK")

    __table_args__ = (
        Index("ix_stock_day_symbol", symbol),
        Index("ix_stock_day_name", name),
        Index("ix_stock_day_timestamp", timestamp.desc()),
    )


def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

# 创建一个全局Session工厂
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def session_factory():
    """返回一个数据库会话实例"""
    return Session()

if __name__ == "__main__":
    engine = init_db(db_url)
    print("数据库表已创建成功")