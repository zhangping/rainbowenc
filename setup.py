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
                        'rainbowenc/passwd']],
                ['/usr/share/rainbowenc/templates',
                        ['rainbowenc/templates/login.html']],
                ['/usr/share/rainbowenc/static',
                        ['rainbowenc/static/gradient.gif',
                        'rainbowenc/static/login_bg.png',
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

