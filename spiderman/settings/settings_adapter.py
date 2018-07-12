from __future__ import absolute_import
from .settings import BaseSettings

class SettingsAdapter(object):
    """
    Wrapps the frontera settings, falling back to scrapy and default settings
    """
    def __init__(self, settings):
        assert isinstance(settings, (type, list))
        self._settings = settings

    def get(self, key, default_value=None):
        for settings in self._settings:
            v = settings.get(key)
            if v is not None: return v

        return None





class ScrapySettingsAdapter(SettingsAdapter):
    def __init__(self, scrapy_settings):
        spiderman_setting_module = scrapy_settings.get('SPIDERMAN_SETTINGS', None)
        spiderman_settings = BaseSettings(spiderman_setting_module)
        super(ScrapySettingsAdapter, self).__init__([scrapy_settings, spiderman_settings])

