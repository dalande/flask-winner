import logging


class Config(object):
    """工程配置信息"""
    pass


class DevelopementConfig(Config):
    """开发模式下的配置"""
    DEBUG = True
    # 默认日志等级
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产模式下的配置"""
    LOG_LEVEL = logging.ERROR


config = {
    "development": DevelopementConfig,
    "production": ProductionConfig
}
