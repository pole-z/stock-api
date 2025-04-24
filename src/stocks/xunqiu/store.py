from datetime import datetime
from decimal import Decimal
from model.stocks import StockDay, Stock
from utils import logger


def stock_save(db_session, stock_data):
    """
    保存股票数据到数据库
    """
    try:
        for item in stock_data:
            stock_data = {
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "net_profit_cagr": Decimal(str(item.get("net_profit_cagr"))) if item.get("net_profit_cagr") not in (None, "") else None,
                "north_net_inflow": Decimal(str(item.get("north_net_inflow"))) if item.get("north_net_inflow") not in (None, "") else None,
                "ps": Decimal(str(item.get("ps"))) if item.get("ps") not in (None, "") else None,
                "type": int(item.get("type")) if item.get("type") not in (None, "") else 0,
                "percent": Decimal(str(item.get("percent"))) if item.get("percent") not in (None, "") else None,
                "has_follow": item.get("has_follow", False),
                "tick_size": Decimal(str(item.get("tick_size"))) if item.get("tick_size") not in (None, "") else None,
                "pb_ttm": Decimal(str(item.get("pb_ttm"))) if item.get("pb_ttm") not in (None, "") else None,
                "float_shares": item.get("float_shares"),
                "current": Decimal(str(item.get("current"))) if item.get("current") not in (None, "") else None,
                "amplitude": Decimal(str(item.get("amplitude"))) if item.get("amplitude") not in (None, "") else None,
                "pcf": Decimal(str(item.get("pcf"))) if item.get("pcf") not in (None, "") else None,
                "current_year_percent": Decimal(str(item.get("current_year_percent"))) if item.get("current_year_percent") not in (None, "") else None,
                "float_market_capital": Decimal(str(item.get("float_market_capital"))) if item.get("float_market_capital") not in (None, "") else None,
                "north_net_inflow_time": datetime.fromtimestamp(item.get("north_net_inflow_time") / 1000) if item.get("north_net_inflow_time") else None,
                "market_capital": Decimal(str(item.get("market_capital"))) if item.get("market_capital") not in (None, "") else None,
                "dividend_yield": Decimal(str(item.get("dividend_yield"))) if item.get("dividend_yield") not in (None, "") else None,
                "lot_size": item.get("lot_size"),
                "roe_ttm": Decimal(str(item.get("roe_ttm"))) if item.get("roe_ttm") not in (None, "") else None,
                "total_percent": Decimal(str(item.get("total_percent"))) if item.get("total_percent") not in (None, "") else None,
                "percent5m": Decimal(str(item.get("percent5m"))) if item.get("percent5m") not in (None, "") else None,
                "income_cagr": Decimal(str(item.get("income_cagr"))) if item.get("income_cagr") not in (None, "") else None,
                "amount": Decimal(str(item.get("amount"))) if item.get("amount") not in (None, "") else None,
                "chg": Decimal(str(item.get("chg"))) if item.get("chg") not in (None, "") else None,
                "issue_date_ts": item.get("issue_date_ts"),
                "eps": Decimal(str(item.get("eps"))) if item.get("eps") not in (None, "") else None,
                "main_net_inflows": Decimal(str(item.get("main_net_inflows"))) if item.get("main_net_inflows") not in (None, "") else None,
                "volume": item.get("volume"),
                "volume_ratio": Decimal(str(item.get("volume_ratio"))) if item.get("volume_ratio") not in (None, "") else None,
                "pb": Decimal(str(item.get("pb"))) if item.get("pb") not in (None, "") else None,
                "followers": int(item.get("followers")) if item.get("followers") not in (None, "") else 0,
                "turnover_rate": Decimal(str(item.get("turnover_rate"))) if item.get("turnover_rate") not in (None, "") else None,
                "mapping_quote_current": Decimal(str(item.get("mapping_quote_current"))) if item.get("mapping_quote_current") not in (None, "") else None,
                "first_percent": Decimal(str(item.get("first_percent"))) if item.get("first_percent") not in (None, "") else None,
                "pe_ttm": Decimal(str(item.get("pe_ttm"))) if item.get("pe_ttm") not in (None, "") else None,
                "dual_counter_mapping_symbol": item.get("dual_counter_mapping_symbol"),
                "total_shares": int(item.get("total_shares")) if item.get("total_shares") not in (None, "") else 0,
                "limitup_days": int(item.get("limitup_days")) if item.get("limitup_days") not in (None, "") else 0 
            }
            
            existing_stock = db_session.query(Stock).filter(
                Stock.symbol == item.get("symbol")
            ).first()
            if existing_stock:
                # 如果股票已存在，则更新数据
                for key, value in stock_data.items():
                    setattr(existing_stock, key, value)
            else:
                # 如果股票不存在，则创建新记录
                stock = Stock(**stock_data)
                db_session.add(stock)
                
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error(f"保存股票数据到数据库出错: {str(e)}")

def stock_day_save(db_session, stock_data, stock_code, stock_name, upsert=False):
    """
    保存股票日K线数据到数据库
    """
    if not stock_data or 'data' not in stock_data or not stock_data['data'].get('item'):
        logger.error(f"股票数据格式不正确: {stock_code}")
        return 0
    
    item_count = 0
    try:
        column_names = stock_data['data']['column']
        items = stock_data['data']['item']
        
        # 检查数据库中是否已存在该股票的K线数据
        existing_records = db_session.query(StockDay.timestamp).filter(
            StockDay.symbol == stock_code
        ).all()
        
        # 将已存在的时间戳转换为集合，用于快速查找
        existing_timestamps = {record[0] for record in existing_records}
        
        for item in items:
            data_dict = dict(zip(column_names, item))
            timestamp = data_dict.get('timestamp')
            
            # 如果该时间戳的数据已存在且不需要更新，则跳过
            if timestamp in existing_timestamps and not upsert:
                # logger.info(f"股票{stock_code}时间戳{timestamp}的数据已存在, 跳过")
                continue
                
            # 创建StockDay对象，注意将数值转换为Decimal类型
            stock_day_data = {
                'symbol': stock_code,
                'name': stock_name,
                'timestamp': timestamp,
                'datetime': datetime.fromtimestamp(timestamp / 1000),
                'volume': data_dict.get('volume'),
                'open': Decimal(str(data_dict.get('open'))) if data_dict.get('open') not in (None, "") else None,
                'high': Decimal(str(data_dict.get('high'))) if data_dict.get('high') not in (None, "") else None,
                'low': Decimal(str(data_dict.get('low'))) if data_dict.get('low') not in (None, "") else None,
                'close': Decimal(str(data_dict.get('close'))) if data_dict.get('close') not in (None, "") else None,
                'chg': Decimal(str(data_dict.get('chg'))) if data_dict.get('chg') not in (None, "") else None,
                'percent': Decimal(str(data_dict.get('percent'))) if data_dict.get('percent') not in (None, "") else None,
                'turnoverrate': Decimal(str(data_dict.get('turnoverrate'))) if data_dict.get('turnoverrate') not in (None, "") else None,
                'amount': Decimal(str(data_dict.get('amount'))) if data_dict.get('amount') not in (None, "") else None,
                'volume_post': Decimal(str(data_dict.get('volume_post'))) if data_dict.get('volume_post') not in (None, "") else None,
                'amount_post': Decimal(str(data_dict.get('amount_post'))) if data_dict.get('amount_post') not in (None, "") else None,
                'pe': Decimal(str(data_dict.get('pe'))) if data_dict.get('pe') not in (None, "") else None,
                'pb': Decimal(str(data_dict.get('pb'))) if data_dict.get('pb') not in (None, "") else None,
                'ps': Decimal(str(data_dict.get('ps'))) if data_dict.get('ps') not in (None, "") else None,
                'pcf': Decimal(str(data_dict.get('pcf'))) if data_dict.get('pcf') not in (None, "") else None,
                'market_capital': Decimal(str(data_dict.get('market_capital'))) if data_dict.get('market_capital') not in (None, "") else None,
                'balance': Decimal(str(data_dict.get('balance'))) if data_dict.get('balance') not in (None, "") else None,
                'hold_volume_cn': Decimal(str(data_dict.get('hold_volume_cn'))) if data_dict.get('hold_volume_cn') not in (None, "") else None,
                'hold_ratio_cn': Decimal(str(data_dict.get('hold_ratio_cn'))) if data_dict.get('hold_ratio_cn') not in (None, "") else None,
                'net_volume_cn': Decimal(str(data_dict.get('net_volume_cn'))) if data_dict.get('net_volume_cn') not in (None, "") else None,
                'hold_volume_hk': Decimal(str(data_dict.get('hold_volume_hk'))) if data_dict.get('hold_volume_hk') not in (None, "") else None,
                'hold_ratio_hk': Decimal(str(data_dict.get('hold_ratio_hk'))) if data_dict.get('hold_ratio_hk') not in (None, "") else None,
                'net_volume_hk': Decimal(str(data_dict.get('net_volume_hk'))) if data_dict.get('net_volume_hk') not in (None, "") else None
            }
            
            # 如果数据已存在且需要更新
            if timestamp in existing_timestamps and upsert:
                existing_record = db_session.query(StockDay).filter(
                    StockDay.symbol == stock_code,
                    StockDay.timestamp == timestamp
                ).first()
                
                # 更新现有记录的所有字段
                for key, value in stock_day_data.items():
                    setattr(existing_record, key, value)
            else:
                # 创建新记录
                stock_day = StockDay(**stock_day_data)
                db_session.add(stock_day)
                
            item_count += 1
            
            # 每500条数据提交一次，避免事务过大
            if item_count % 500 == 0:
                db_session.commit()
        
        # 提交剩余的数据
        if item_count % 500 != 0:
            db_session.commit()
            
        logger.info(f"成功保存 {item_count} 条 {stock_name}({stock_code}) 数据到数据库")
    except Exception as e:
        db_session.rollback()
        logger.error(f"保存数据到数据库出错: {str(e)}")
    
    return item_count