import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'NCKU OIA Announcement Crawler'
copyright = '2024, LIM JIA QUAN'
author = 'LIM JIA QUAN'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 語言設置
language = 'zh_TW' 