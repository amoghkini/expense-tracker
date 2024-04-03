import os
from config.settings import BaseConfig


ROOT_PATH = BaseConfig.ROOT_PATH


def extract_settings(config):
    rtn = []
    for itm in sorted(dir(config)):
        if not itm.startswith('_') and itm == itm.upper():
            rtn.append((itm,getattr(config,itm)))
    return tuple(rtn)


def is_dir(name):
    return os.path.isdir(os.path.join(ROOT_PATH,name))


def common_context():
    return {
        'getattr':getattr,
        'extract_settings':extract_settings,
        'str':str,
        'zip':zip,
        'is_dir':is_dir,
        'my_email': 'kyle@level2designs.com',
        'type': type,
        'dir': dir,
        'get_name': _get_name,
        'use_editor': False,
        'config':BaseConfig,
        'map':map,
    }
    
def get_current_user():
    # In a real application, you would retrieve the current user from the session or database
    return {'username': 'John Doe'}

# Define a context processor function
def inject_user():
    # Assuming you have a way to get the current user, such as from a session
    user = get_current_user()
    return dict(user=user)

def _get_name():
    user = get_current_user()
    return dict(user=user)

        

def inject_layout_type():
    return {'layout_type': 'sidebar'}  # You can dynamically set the layout type here