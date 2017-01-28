## IMPORTS

from plugins.info import PluginInfo

## ALL DECLARATION

__all__ = (
    'info',
    )

## INFO

info = PluginInfo(
    'warcraft',
    verbose_name='Warcraft Global Offensive',
    author='Thomas "Predz" Vieth',
    description='A plugin for the SourcePython API, which extends the attributes of a'
        ' player in the source engine.',
    version=1.0,
    url='http://www.warcraft-source.com/'
)