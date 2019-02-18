
import os

# 项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 静态文件
STATIC_PATH = os.path.join(BASE_DIR, 'static')

# 模板文件
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

# 上传图片地址
MEDIA_PATH = os.path.join(STATIC_PATH, 'media')
UPLOAD_FOLDER = os.path.join(MEDIA_PATH, 'upload')