from stocks.browser import Browser
from stocks.exception import StockBrowserException, StockDataException
from utils import logger, cache_func


def stock_init(user_agent):
    """
    1. 先加载 https://xueqiu.com/
    2. 再加载 https://xueqiu.com/S/SH000001
    """
    browser = Browser(headless=True, user_agent=user_agent)
    page = browser.get_page()
    response = page.goto("https://xueqiu.com/")
    if response.status != 200:
        raise Exception(f"访问雪球首页失败，HTTP状态码: {response.status}")
    page.wait_for_load_state("networkidle")

    response = page.goto("https://xueqiu.com/S/SH000001")
    if response.status != 200:
        raise Exception(f"访问雪球股票页面失败，HTTP状态码: {response.status}")
    page.wait_for_load_state("networkidle")
    page.wait_for_load_state("domcontentloaded")
    
    return browser

@cache_func(expire=3600)
def get_cookie(user_agent):
    """
    1. 先加载 https://xueqiu.com/
    2. 再加载 https://xueqiu.com/S/SH000001
    3. 获取cookie
    """
    browser = None
    try:
        browser = stock_init(user_agent)
        cookies = browser.get_cookie()
        logger.debug(f"获取到的cookie: {cookies}")
        
        return cookies
    except Exception as e:
        logger.error(f"获取雪球cookie失败: {e}")
        raise StockBrowserException("xunqiu", e) 
    finally:
        if browser:
            browser.close()

@cache_func(expire=3600)
def get_stock_profile(stock_code: str, user_agent: str):
    """
    获取股票-公司简介
    """
    browser = None
    try:
        browser = stock_init(user_agent)
        page = browser.new_page()
        url = f"https://xueqiu.com/snowman/S/{stock_code}/detail#/GSJJ"
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.wait_for_load_state("domcontentloaded")
        #html = page.content()

        # Xpath 获取公司简介
        profile = {}
        table_rows = page.locator('//*[@id="app"]/div[2]/div[2]/div/div[2]/div/table/tbody/tr')
        count = table_rows.count()
        logger.info(f"获取到的公司简介行数: {count}")
        
        print(table_rows)
        for i in range(count):
            row = table_rows.nth(i)
            cells = row.locator('td')
            cell_count = cells.count()
            
            if cell_count >= 2:
                label_cell = cells.nth(0)
                value_cell = cells.nth(1)
                
                label_text = label_cell.text_content()
                profile[label_text] = value_cell.text_content()
                logger.info(f"获取到的{label_text}: {profile[label_text]}")
        
        return profile
    except Exception as e:
        raise StockDataException("xunqiu", str(e), f"获取股票{stock_code}简介失败")
    finally:
        if browser:
            browser.close()


def get_stock_listing_date(stock_code: str, user_agent: str):
    """
    获取股票-上市日期
    """
    
    stock_profile = get_stock_profile(stock_code, user_agent)
    return stock_profile.get("上市日期")