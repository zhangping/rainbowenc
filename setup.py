from setuptools import setup, find_packages

# Dynamically calculate the version based on rainbowenc.VERSION.
version = __import__('rainbowenc').get_version()

setup(
        name = "Rainbowenc",
        version = version,
        url = 'http://www.rainbowenc.org/',
        author = 'Zhang Ping',
        author_email = 'dqzhangp@163.com',
        description = 'A real time encoder based on gstreamer',
        packages = find_packages (),
        install_requires = [
                'web.py',],
        data_files = [
                ['/usr/share/rainbowenc',
                        ['rainbowenc/rainbow.py',
                        'rainbowenc/genpage.py',
                        'rainbowenc/systat.py',
                        'rainbowenc/passwd']],
                ['/usr/share/rainbowenc/templates',
                        ['rainbowenc/templates/login.html',
                        'rainbowenc/templates/rainbow.html']],
                ['/usr/share/rainbowenc/static',
                        ['rainbowenc/static/gradient.gif',
                        'rainbowenc/static/login_bg.png',
                        'rainbowenc/static/header_logo.png',
                        'rainbowenc/static/navbar_default.gif',
                        'rainbowenc/static/navbar_active.gif',
                        'rainbowenc/static/header_bg.png',
                        'rainbowenc/static/gradient.gif',
                        'rainbowenc/static/listtopic_bg.png',
                        'rainbowenc/static/vncell_bg.png',
                        'rainbowenc/static/header_rlogo.png',
                        'rainbowenc/static/navbar.js',
                        'rainbowenc/static/gui.js',
                        'rainbowenc/static/navbar.css',
                        'rainbowenc/static/tabs.css',
                        'rainbowenc/static/gui.css']],],
        classifiers = [
                'Development Status :: Under development',
                'Intended Audience :: Users',
                'License :: GPL License',
                'Operating System :: Linux',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.5',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
        ],
)

