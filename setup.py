from distutils.core import setup
import os

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
rainbowenc_dir = 'rainbowenc'

for dirpath, dirnames, filenames in os.walk(rainbowenc_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Dynamically calculate the version based on rainbowenc.VERSION.
version = __import__('rainbowenc').get_version()

setup(
    name = "Rainbowenc",
    version = version,
    url = 'http://www.rainbowenc.org/',
    author = 'Zhang Ping',
    author_email = 'dqzhangp@163.com',
    description = 'A real time encoder based on gstreamer',
    #download_url = '',
    packages = packages,
    data_files = data_files,
    scripts=['rainbowenc/rainbowenc.py'],
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

