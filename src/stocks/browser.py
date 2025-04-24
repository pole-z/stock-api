from playwright.sync_api import sync_playwright

class Browser:
    def __init__(self, headless=True, user_agent=None):
        self.playwright = sync_playwright().start()
        # 创建浏览器上下文，隐藏自动化特征
        self.browser = self.playwright.chromium.launch(headless=headless, args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-site-isolation-trials',
            '--no-sandbox',
            '--disable-web-security'
        ])
        
        # 创建上下文以隐藏指纹特征
        self.context = self.browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1.0,
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            permissions=['geolocation'],
            java_script_enabled=True,
            bypass_csp=True,
            has_touch=False
        )
        
        # 修改WebDriver状态，隐藏自动化标记
        self.page = self.context.new_page()
        self.page.add_init_script(self.__scripts())
    
    def __scripts(self):
        return """
            // 隐藏WebDriver特征
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
            
            // 模拟正常浏览器插件
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
                    { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                    { name: 'Native Client', filename: 'internal-nacl-plugin' }
                ],
            });
            
            // 模拟Chrome浏览器特性
            window.chrome = {
                runtime: {},
                app: { isInstalled: false },
                webstore: { onInstallStageChanged: {}, onDownloadProgress: {} },
                csi: function(){},
                loadTimes: function(){}
            };
            
            // 修改语言特征
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
            
            // 隐藏Automation特征
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        """

    def get_browser(self):
        """获取浏览器"""
        return self.browser

    def get_page(self):
        """获取页面"""
        return self.page
    
    def get_context(self):
        """获取上下文"""
        return self.context
    
    def new_page(self):
        """创建新的页面"""
        return self.context.new_page()

    def get_cookie(self):
        """获取cookie"""
        return self.context.cookies()
    
    def close(self):
        """关闭浏览器和playwright"""
        try:
            if self.page and not self.page.is_closed():
                self.page.close()
            
            if self.context:
                self.context.close()
                
            if self.browser:
                self.browser.close()
                
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"关闭浏览器时出错: {e}")
