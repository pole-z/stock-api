import requests
from stocks.exception import StockException, StockLoginException
from stocks.xunqiu.html import get_cookie, get_stock_profile
from stocks.xunqiu.api import XunqiuStockApi
from stocks.xunqiu.store import stock_day_save
from utils import logger
from utils.cache import cache_clear

MAX_RETRY = 1

def create_xunqiu_client(user_agent, retry=0):
    """
    创建雪球客户端
    
    1. 获取cookie
    2. 创建session
    3. 创建API客户端
    
    返回: XunqiuStockApi 实例
    """

    try:
        cookies = get_cookie(user_agent)
        
        # 创建会话并设置cookie
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"])
        
        # ## 临时Debug cookie
        # cookieStr = "cookiesu=381720599629237; device_id=47ddb5d165bf5819631c67e51e1de620; s=cw11ypmj40; xq_a_token=aa62cf737ae9d7f029c65a6ce6adc6af252a295b; xqat=aa62cf737ae9d7f029c65a6ce6adc6af252a295b; xq_r_token=6726ffd46c8b0facc9034c6fd6f26abf2cde8e40; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjY0MTEwMDMyNDMsImlzcyI6InVjIiwiZXhwIjoxNzQ3NDYzNjQ1LCJjdG0iOjE3NDQ4NzE2NDUwNjgsImNpZCI6ImQ5ZDBuNEFadXAifQ.jEsFsXj0Ve_UQ9UdSjLB08F-6ZY2yZpMW2b2bxXRzh0urG9CGnsixak2THgzsbc6E4q8uT0z5TEgSyOOOpKEd_hehKQN3PrQ4E6Eqqe1tKxV2-MU8XRYbL3gkyohiqXOOGAdi8rIgk4TfPZEikVRdaD-mcOLVJlWuNue8XAEX99MXwJ0z2BO33_0LrTSZt_7w6nZ17TFj4XLAtVO6-lW2m3pW9Kt3wtgkzn7g6Pql0TglrCjDV1zCIPR_EnrN3uhlwrIg14GW1h22RCOBdyBxCmDYb6Q5hMwsOjKum0B1yTRaUZWJfwg_XEGpz9uBP60oXDoFKCYVozETt3T9Zv4bg; xq_is_login=1; u=6411003243; is_overseas=0; ssxmod_itna=Qq0x2D0DnDcGoY5i7KYwDYq4mxdyeDzxC5iOD+xQ5K08D6jxBRiCHAx0==kiD9AC0Dwzh3CqDs4qxiNDAg40iDC3mdGYUcq54KKfmCqtYK3+DyImvoD9rRd3ttD1Xz2=wt5Ai34xB3DExGkRpaYDemWDCeDQxirDD4DA7YD=xDrD0Rwa8gwDYpe7W4DXPBwo4GCbDDC=Z5Dwp+mf38EElywf9fepDDkDlPD6abG7QSL4tSwdUYDFrgwaewxcDi3840TLbQwNfiQZWZrotSADCFXplYDoPBL2Yova5RK0asY7hPqo=GxeDh4i0D/2zfDxYiZ90K7DZQ0DUiNiGO04OAY/4xDG+zeOqHWxe+Cvd1ju12Ye+Az5Ohc2D5gQ5hh1O+IoxhD5yi5QG5ZAdaiNQD4/ixvrvHm54D; ssxmod_itna2=Qq0x2D0DnDcGoY5i7KYwDYq4mxdyeDzxC5iOD+xQ5K08D6jxBRiCHAx0==kiD9AC0Dwzh3e4DWhBWW2KDLDxSKDl6EGux3C9C8X=YC3jvu=k0=PK+vUQAD5FCeiQZ=M6vM=0oxjWPfZL/fS6z+8qKBE5n7GxjDkDqI4jvbGhfCS2Y5utGIRD/KM0uCOGxKq+5E4KCDwx6Ge69Il2xFeQMGcPPQ0o9B1DaufyeenHQdtn+cf2h+1djfct/GPj2D9OZtAYeShDrYKBHOn2Uo0usyilKoihi4xhyw5vknxrs70G3DozB=GsxD"
        # # 将字符串形式的cookie转换为RequestsCookieJar对象
        # cookie_jar = requests.cookies.RequestsCookieJar()
        # for item in cookieStr.split('; '):
        #     if item:
        #         name, value = item.split('=', 1)
        #         cookie_jar.set(name, value)
        # session.cookies.update(cookie_jar)
        # ## 
        
        return XunqiuStockApi(session)
    
    except StockLoginException as e:
        logger.error(f"雪球cookie失效: {e}")
        # 清除缓存, 重新获取Cookies
        cache_clear()
        return create_xunqiu_client(user_agent)
    except StockException as e:
        raise e
    except Exception as e:
        if retry < MAX_RETRY:
            create_xunqiu_client(user_agent, retry=retry+1)
        else:
            raise StockException("雪球客户端创建失败", "xunqiu", e)

__all__ = [
    "get_cookie",
    "get_stock_profile",
    "XunqiuStockApi",
    "create_xunqiu_client",
    "stock_day_save",
]