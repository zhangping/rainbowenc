from distutils.core import setup

# Dynamically calculate the version based on rainbowenc.VERSION.
version = __import__('django').get_version()

setup(
    name = "Rainbowenc",
    version = version,
    url = 'http://www.rainbowenc.org/',
    author = 'Zhang Ping',
    author_email = 'dqzhangp@163.com',
    description = 'A real time encoder based on gstreamer',
    #download_url = '',
    packages = packages,
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

