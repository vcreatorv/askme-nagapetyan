# Привязка к порту
bind = '127.0.0.1:8000'

# Количество рабочих процессов
workers = 2

# Дополнительные настройки
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2


accesslog = '/var/tmp/askme_nagapetyan.gunicorn.log'