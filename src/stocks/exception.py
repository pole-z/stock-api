from utils import logger

class StockException(Exception):
    """股票异常"""
    def __init__(self, stock, message, code=500):
        self.message = message
        self.code = code
        logger.error(f"code: {self.code}, 股票{stock}异常: {self.message}")


class StockBrowserException(StockException):
    """股票浏览器异常"""
    def __init__(self, stock, message, code=500):
        message = f"浏览器异常: {message}"
        super().__init__(stock, message, code)

class StockLoginException(StockException):
    """股票登录异常"""
    def __init__(self, stock, response, message, code=500):
        message = f"登录异常: {message}"
        super().__init__(stock, message, code)


class StockResponseException(StockException):
    """股票响应异常"""
    def __init__(self, stock, response, message, code=500):
        message = f"响应异常: {message}, 响应: {response}"
        super().__init__(stock, message, code)


class StockDataException(StockException):
    """股票数据异常"""
    def __init__(self, stock, data, message, code=500):
        message = f"数据异常: {message}, 数据: {data}"
        super().__init__(stock, message, code)
