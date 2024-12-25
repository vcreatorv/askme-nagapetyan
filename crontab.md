## Настройка Cron для автоматического обновления кэша

Чтобы автоматически обновлять кэш для популярных тегов и лучших пользователей, настройте Cron следующим образом:

1. Откройте редактор Cron:

   ```bash
   crontab -e
   ```

2. Добавьте следующие строки:

   ```bash
   * * * * * cd /usr/local/share/web/askme-nagapetyan && /usr/local/share/web/askme-nagapetyan/venv/bin/python manage.py cache_popular_tags
   * * * * * cd /usr/local/share/web/askme-nagapetyan && /usr/local/share/web/askme-nagapetyan/venv/bin/python manage.py cache_top_users
   ```

Эти строки запускают команды обновления кэша каждую минуту. Можно настроить другой интервал, изменив формат Cron. Примеры можно посмотреть [здесь](https://crontab.guru/examples.html).

