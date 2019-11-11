import pytest
from django.conf import settings
from django.test import Client
import os


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'test_db.sqlite3'),
    }
    with django_db_blocker.unblock():
        pass


@pytest.fixture(scope='session')
def proxy_client(django_db_setup):
    client = Client()
    yield client


@pytest.fixture(scope='session', autouse=True)
def shutdown():
    yield
    # 指定 pytest 执行完后的操作
    # MessageEngine.instance().shutdown()
    # MsgThreadPool.instance().shutdown()
