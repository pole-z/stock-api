import time
import subprocess
import sys
import concurrent.futures
from utils import logger
from model.stocks import Stock, StockDay, session_factory
from stocks.xunqiu import create_xunqiu_client
from stocks.xunqiu.store import stock_day_save, stock_save

# 雪球用户代理
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64; x64; rv:134.0) Gecko/20100101 Firefox/134.0"
# 并行处理线程数
MAX_WORKERS = 10

def check_dependencies():
    """检查并安装依赖"""
    try:
        # 检查依赖是否已安装
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "src/requirements.txt"])
        logger.info("依赖检查完成")
        
        # 安装 playwright 浏览器
        try:
            import playwright
            subprocess.check_call([sys.executable, "-m", "playwright", "install"])
            logger.info("Playwright 浏览器安装完成")
        except ImportError:
            logger.error("Playwright 未安装，请先安装依赖")
            return False
        except Exception as e:
            logger.error(f"Playwright 浏览器安装失败: {e}")
            return False
        return True
    except Exception as e:
        logger.error(f"依赖安装失败: {e}")
        return False

def collect_stock_lists(client, db_session):
    """收集股票列表数据"""
    try:
        # 采集沪深市场
        stock_list = client.get_stock_list_all("sh_sz")
        logger.info(f"沪深股票数量: {len(stock_list)}")
        stock_save(db_session, stock_list)
        
        # 采集北交所
        stock_list = client.get_stock_list_all("bj")
        logger.info(f"北交所股票数量: {len(stock_list)}")
        stock_save(db_session, stock_list)
        return True
    except Exception as e:
        logger.error(f"采集股票列表数据失败: {e}")
        return False

def process_stock(stock):
    """处理单个股票数据，每个线程使用独立的数据库会话和客户端"""
    try:
        # 每个线程创建自己的会话和客户端
        local_session = session_factory()
        local_client = create_xunqiu_client(USER_AGENT)
        
        stock_code = stock.symbol
        stock_name = stock.name
        
        # 获取最新的股票日数据
        stock_day = local_session.query(StockDay)\
            .filter(StockDay.symbol == stock_code)\
            .order_by(StockDay.timestamp.desc())\
            .first()
            
        upsert = False
        # 没有数据, 采集所有数据, 反之采集最近10条数据
        if not stock_day:
            last_timestamp = int(time.time()) * 1000
            stock_data = local_client.get_stock_kline_all(stock_code=stock_code, begin=last_timestamp)
        else:
            last_timestamp = stock_day.timestamp
            stock_data = local_client.get_stock_kline(stock_code=stock_code, begin=last_timestamp, count=10)
            upsert = True

        if stock_data:
            try:
                stock_day_save(local_session, stock_data, stock_code, stock_name, upsert)
                local_session.commit()
                return True
            except Exception as e:
                local_session.rollback()
                logger.error(f"保存股票 {stock_name}({stock_code}) 数据失败，已回滚: {e}")
                return False
        return True
    except Exception as e:
        logger.error(f"处理股票 {stock.name}({stock.symbol}) 数据失败: {e}")
        return False
    finally:
        # 确保关闭会话
        if 'local_session' in locals():
            local_session.close()

def process_stocks_parallel(stocks):
    """并行处理多个股票数据，每个线程使用独立的数据库连接"""
    success_count = 0
    failure_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 不再传递共享的client和db_session
        futures = {executor.submit(process_stock, stock): stock for stock in stocks}
        for future in concurrent.futures.as_completed(futures):
            stock = futures[future]
            try:
                if future.result():
                    success_count += 1
                else:
                    failure_count += 1
            except Exception as e:
                logger.error(f"处理股票 {stock.name}({stock.symbol}) 时发生异常: {e}")
                failure_count += 1
    
    return success_count, failure_count

def main():
    """主函数"""
    # 检查依赖
    if not check_dependencies():
        logger.error("依赖检查失败，程序退出")
        return
    
    try:
        # 创建数据库会话和客户端
        db_session = session_factory()
        client = create_xunqiu_client(USER_AGENT)
        
        # # 收集股票列表
        # if not collect_stock_lists(client, db_session):
        #     logger.error("采集股票列表失败，跳过股票数据采集")
        #     return
        
        # 获取所有股票并处理
        stock_list = db_session.query(Stock).all()
        logger.info(f"开始采集 {len(stock_list)} 只股票的历史数据")
        
        # 不再向并行处理函数传递client和db_session
        success_count, failure_count = process_stocks_parallel(stock_list)
        
        logger.info(f"股票数据采集完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        
    except Exception as e:
        logger.exception(f"保存数据到数据库出错: {e}")
    finally:
        # 确保会话被关闭
        if 'db_session' in locals():
            db_session.close()

if __name__ == "__main__":
    logger.info("开始采集股票数据")
    main()