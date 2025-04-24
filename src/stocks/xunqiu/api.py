from datetime import datetime
import json
import time
from typing import Union
import requests

from stocks.exception import StockLoginException, StockResponseException
from utils import logger

UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

headers = {
    "User-Agent": UserAgent,
    "Accept": "application/json, text/plain, */*",
}

class XunqiuStockApi:
    """
    雪球A股API
    """
    
    def __init__(self, session: requests.Session):
        self.session = session

    def _make_request(self, url: str, event_name: str):
        """
        发送请求并处理错误
        """
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code != 200:
                raise StockLoginException("xunqiu", response, f"{event_name}，状态码：{response.status_code}")
            return response.json()
        except requests.RequestException as e:
            raise StockResponseException("xunqiu", None, f"{event_name}，网络错误：{str(e)}")

    def get_stock_batch_quote(self, stock_codes: Union[list, set, tuple, str]):
        """
        批量搜索股票
        """
        if isinstance(stock_codes, (list, set, tuple)):
            stock_codes = ",".join(stock_codes)
        
        url = f"https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol={stock_codes}"
        return self._make_request(url, "获取股票批量检索")
    
    def get_stock_quote(self, stock_code: str):
        """
        搜索一只股票
        """
        url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={stock_code}"
        return self._make_request(url, "获取股票")

    def get_stock_list(self, type="sh_sz", page=1, size=90):
        """
        获取股票列表
        type 股票类型 sh_sz 沪深  bj 北交所
        page 30 60 90
        """
        url = f"https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size={size}&order=desc&order_by=percent&market=CN&type={type}"
        return self._make_request(url, "获取股票列表")
    
    def get_stock_detail(self, stock_code: str):
        """
        获取股票详情
        """
        url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={stock_code}&extend=detail"
        return self._make_request(url, "获取股票详情")

    def get_stock_kline(self, stock_code: str, begin=None, count=-284, period="day", type="before", indicator="kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"):
        """
        获取股票K线数据
        
        参数说明:
        - stock_code: 股票代码，如SH601086
        - begin: 开始时间戳(毫秒)，默认为当前时间
        - count: 获取数据数量，默认-284(表示获取284条历史数据)
        - period: 周期类型，可选值:
            - 分时: 1d(一日), 5d(五日)
            - K线: day(日), week(周), month(月), quarter(季), year(年)
            - 分钟K线: 1m, 5m, 15m, 30m, 60m, 120m
        - type: 复权:
            - before: 前复权, 默认
            - after: 后复权
            - normal: 不复权
        - indicator: 指标数据，默认包含kline,pe,pb等多个指标
        
        示例URL:
        分时线: https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH601086&period=1d
        日K线: https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH601086&begin=1744792793806&period=day&type=before&count=-284&indicator=kline
        """
        begin = begin or int(datetime.now().timestamp() * 1000)
        
        # 判断是否为分时图
        if period in ['1d', '5d']:
            url = f"https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol={stock_code}&period={period}"
        else:
            url = f"https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={stock_code}&begin={begin}&period={period}&type={type}&count={count}&indicator={indicator}"
        
        return self._make_request(url, "获取股票K线数据")

    def get_stock_volume_detail(self, stock_code: str, count=10):
        """
        成交明细Lv1
        """
        url = f"https://stock.xueqiu.com/v5/stock/history/trade.json?symbol={stock_code}&count={count}"
        return self._make_request(url, "获取股票成交明细")
    
    def get_stock_market(self, stock_code: str):
        """
        五档盘口
        """
        url = f"https://stock.xueqiu.com/v5/stock/realtime/pankou.json?symbol={stock_code}"
        return self._make_request(url, "获取股票五档盘口")
    

    def get_stock_list_all(self, type):
        """
        获取所有股票列表
        """
        stocks = []
        page = 1
        while True:
            stock_list = self.get_stock_list(type, page=page)
            total_stock = stock_list.get("data", {}).get("count")
            
            stocks.extend(stock_list.get("data", {}).get("list", {}))
            logger.info(f"股票数量:{total_stock}, 当前页{page}, 已采集数量:{len(stocks)}")
            if len(stocks) >= total_stock:
                break
            page += 1
        return stocks

    
    def get_stock_kline_all(self, stock_code: str, begin=None, count=-284, period="day", type="before", indicator="kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"):
        """
        获取股票K线所有历史数据
        
        参数说明:
        - stock_code: 股票代码，如SH601086
        - begin: 开始时间戳(毫秒)，默认为当前时间
        - count: 获取数据数量，负数表示获取历史数据
        - period: 周期类型，默认为day(日K线)
        - type: 复权类型，默认为before(前复权)
        - indicator: 指标数据
        
        返回:
        包含完整历史K线数据的字典
        """
        result = []
        column = None
        
        while True:
            # 获取一批K线数据
            data = self.get_stock_kline(stock_code, begin, count, period, type, indicator)
            items = list(data.get("data", {}).get("item", []))
            
            # 如果没有数据则退出循环
            if not items:
                break

            # 保存列名
            if column is None:
                column = data.get("data", {}).get("column", [])

            # 去重并按时间排序
            tmp = {item[0]: item for item in items}
            
            # 计算下一次查询的起始时间
            if count < 0:
                begin = items[0][0]  # 向前查询时，使用最早的时间戳
                sorted_result = [tmp[key] for key in sorted(tmp.keys(), reverse=True)] if tmp else []
            else:
                begin = items[-1][0]  # 向后查询时，使用最晚的时间戳
                sorted_result = [tmp[key] for key in sorted(tmp.keys())] if tmp else []

            result.extend(sorted_result)
            
            # 记录日志
            begin_date = datetime.fromtimestamp(items[0][0]/1000).strftime("%Y-%m-%d")
            end_date = datetime.fromtimestamp(items[-1][0]/1000).strftime("%Y-%m-%d")
            logger.debug(f"获取股票:{stock_code}, {period}K线, {begin_date}至{end_date}, 累计{len(result)}条数据")
            
            # 如果返回的数据量小于请求的数量，说明已经没有更多数据
            if len(items) < abs(count):
                break
        
        return {
            "data": {
                "column": column,
                "item": result
            }
        }
