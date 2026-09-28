# Результаты проверки

Проверка выполнена 29 сентября 2026 года. Временная среда создавалась в Yandex Cloud и была полностью удалена после теста.

## Статические проверки

| Проверка | Результат |
|---|---|
| Генерация диаграмм `python3 diagrams/generate.py --check` | пройдена |
| XML-разбор всех SVG | пройден |
| Компиляция `diagrams/generate.py` | пройдена |
| `terraform fmt -check` | пройдена |
| `terraform init -backend=false` | пройдена |
| `terraform validate` | пройдена |
| Проверка внутренних Markdown-ссылок | пройдена |
| Поиск секретов и незавершённых маркеров | пройден |

## Облачный прогон

Версии: Terraform 1.5.7, `yandex-cloud/yandex` 0.220.0.

1. `terraform plan`: `5 to add, 0 to change, 0 to destroy`.
2. `terraform apply`: `Resources: 5 added, 0 changed, 0 destroyed`.
3. HTTP smoke-тест вернул страницу `Future 2.0 Data Portal`, созданную через cloud-init.
4. Повторный `terraform plan -detailed-exitcode`: `No changes`, exit code `0`.
5. `terraform destroy`: `Resources: 5 destroyed`.
6. После удаления state пуст, ресурсов с тестовым префиксом среди VM и дисков нет, а счётчики консоли вернулись к исходным значениям.

Доказательства прогона находятся в [`Task4/evidence`](Task4/evidence/).
