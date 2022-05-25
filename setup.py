try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A toy interactive C++ interpreter',
    'author': 'Tiensbakung',
    'url': '#URL to get it.#',
    'download_url': '#Where to download it#',
    'author_email': 'Tiensbakung@googlemail.com',
    'version': '#0.1#',
    'install_requires': [],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'interc'
}

setup(**config)
