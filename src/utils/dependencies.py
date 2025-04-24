import os
import subprocess
import sys

def check_dependencies():
    """检查并安装依赖"""
    try:
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        requirements_path = os.path.join(current_dir, "src", "requirements.txt")
            
        # 检查依赖是否已安装
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("依赖检查完成")
        
        # 安装 playwright 浏览器
        try:
            import playwright
            subprocess.check_call([sys.executable, "-m", "playwright", "install"])
            print("Playwright 浏览器安装完成")
            subprocess.check_call([sys.executable, "-m", "playwright", "install-deps"])
            print("Playwright 依赖安装完成")           
        except ImportError:
            print("Playwright 未安装，请先安装依赖")
            return False
        except Exception as e:
            print(f"Playwright 浏览器安装失败: {e}")
            return False
        return True
    except Exception as e:
        print(f"依赖安装失败: {e}")
        return False

# 在模块导入时自动执行依赖检查
_dependencies_checked = False

def ensure_dependencies():
    """确保依赖已经检查并安装"""
    global _dependencies_checked
    if not _dependencies_checked:
        if not check_dependencies():
            raise ImportError("依赖检查失败，请检查错误信息并重试")
        _dependencies_checked = True

# 模块导入时执行依赖检查
ensure_dependencies() 