# 股票数据API

这是一个用于获取中国股票市场数据的Python API工具，目前支持从雪球(Xunqiu)获取A股数据。

## 功能特点

- 支持获取沪深和北交所股票列表
- 支持获取股票实时行情和详细信息
- 支持获取股票K线数据（日K、周K、月K等）
- 支持获取股票交易明细和盘口数据
- 支持数据存储和缓存

## 安装

### 前置条件

- Python 3.6+
- pip

### 安装步骤

1. 克隆代码库
```bash
git clone https://github.com/your-username/stock-api.git
cd stock-api
```

2. 安装依赖
```bash
pip install -r src/requirements.txt
```

## 项目结构

```
src/
├── stocks/              # 股票API核心模块
│   ├── xunqiu/          # 雪球API实现
│   │   └── api.py       # 雪球API接口
│   ├── browser.py       # 浏览器模拟模块
│   ├── exception.py     # 异常处理类
│   └── base.py          # API基类
├── model/               # 数据模型
├── utils/               # 工具函数
├── collect.py           # 数据采集脚本
├── requirements.txt     # 项目依赖
└── test.py              # 测试脚本
```

## 使用方法

### 创建API客户端

```python
from stocks.xunqiu import create_xunqiu_client

# 创建雪球API客户端
client = create_xunqiu_client()
```

### 获取股票列表

```python
# 获取沪深股票列表
sh_sz_stocks = client.get_stock_list_all("sh_sz")

# 获取北交所股票列表
bj_stocks = client.get_stock_list_all("bj")
```

### 获取单只股票信息

```python
# 获取股票详情
stock_detail = client.get_stock_detail("SH601086")  # 中国国航

# 获取股票实时行情
stock_quote = client.get_stock_quote("SH601086")
```

### 获取K线数据

```python
# 获取日K线数据
daily_kline = client.get_stock_kline(
    stock_code="SH601086",  # 股票代码
    period="day",           # 周期类型：day(日)、week(周)、month(月)等
    type="before"           # 复权类型：before(前复权)、after(后复权)、normal(不复权)
)

# 获取完整历史K线数据
full_kline = client.get_stock_kline_all(
    stock_code="SH601086",
    period="day",
    type="before"
)
```

### 获取成交明细和盘口数据

```python
# 获取成交明细
trade_detail = client.get_stock_volume_detail("SH601086", count=10)

# 获取五档盘口
market_detail = client.get_stock_market("SH601086")
```

## K线数据说明

`get_stock_kline` 方法参数说明:

- `stock_code`: 股票代码，如SH601086
- `begin`: 开始时间戳(毫秒)，默认为当前时间
- `count`: 获取数据数量，默认-284(表示获取284条历史数据)
- `period`: 周期类型:
  - 分时: 1d(一日), 5d(五日)
  - K线: day(日), week(周), month(月), quarter(季), year(年)
  - 分钟K线: 1m, 5m, 15m, 30m, 60m, 120m
- `type`: 复权类型:
  - before: 前复权(默认)
  - after: 后复权
  - normal: 不复权
- `indicator`: 指标数据，默认包含kline,pe,pb等多个指标

## 异常处理

API提供了以下异常类型:

- `StockException`: 基础股票异常
- `StockBrowserException`: 浏览器异常
- `StockLoginException`: 登录异常
- `StockResponseException`: API响应异常
- `StockDataException`: 数据处理异常

## 示例

```python
from stocks.xunqiu import create_xunqiu_client
from utils import logger

try:
    # 创建客户端
    client = create_xunqiu_client()
    
    # 获取股票信息
    stock_code = "SH601086"  # 中国国航
    stock_detail = client.get_stock_detail(stock_code)
    print(f"股票名称: {stock_detail['data']['quote']['name']}")
    
    # 获取K线数据
    kline_data = client.get_stock_kline_all(stock_code, period="day")
    print(f"获取到{len(kline_data['data']['item'])}条K线数据")

except Exception as e:
    logger.exception(f"操作失败: {e}")
```

## 许可证

[MIT](LICENSE)
