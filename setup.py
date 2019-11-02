# encoding='utf-8'
from setuptools import setup, find_packages


setup(
    name='mysite_3',
    version='${version}',
    description='Blog System base on Django',
    author='godlike',
    author_email='thefivefire@gmail.com',
    url='https://www.the5fire.com',
    license='MIT',
    packages=find_packages('mysite_3'),
    include_package_data=True,
    install_requires=[
        'django==1.11',
        'gunicorn==19.8.1',
        'supervisor==4.0.0',
        'xadmin==0.6.1',
        'mysqlclient==1.3.12',
        'django-ckeditor==5.4.0',
        'django-rest-framework==0.1.0',
        'django-redis==4.8.0',
        'django-autocomplete-light==3.2.10',
        'mistune==0.8.3',
        'Pillow==6.2.0',
        'coreapi==2.3.3',
        'django-redis==4.8.0',
        'hiredis==0.2.0',
        # debug
        'django-debug-toolbar==1.9.1',
        'django-silk==2.0.0',
    ],
    scripts=[
        'manage.py',
        'mysite_3/wsgi.py',
    ],
    entry_points={
        'console_scripts': [
            'mysite_3_manage = manage:main',
        ]
    },

)