# Роадмап трансформации на 12 месяцев

## Этапы

| Срок | Работы | Ожидаемый результат | Ответственные | Ресурсы | Бизнес-цель / зачем |
|---|---|---|---|---|---|
| 0–2 мес. **Основание** | утвердить C4/DFD, домены, классификацию; создать landing zone и Terraform-модули; ввести SLO, catalog skeleton, data-contract template; снять baseline по 10 ключевым отчётам | согласованное целевое решение; границы и владельцы; dev/test в облаке; реестр PII/PHI/PCI; метрики As-Is | Lead Architect, CISO/DPO, Cloud Platform Lead, domain owners | 1 architect, 2 platform, 1 security, 1 data governance; облачный sandbox и обучение | снять архитектурную неопределённость; не получить штрафы/утечку при миграции |
| 2–4 мес. **Платформенный MVP** | развернуть Object Storage/Iceberg, Kafka, Query Engine, orchestrator, catalog, IAM/ABAC, observability; подключить CDC от SQL Server через anti-corruption layer | технический вертикальный срез; 2 пилотных продукта: `clinic-capacity` и `portfolio-daily`; параллельная сверка | Data Platform Lead, Clinic Data PO, Fintech Data PO, SRE | 5 data/platform engineers, 2 domain engineers, 1 SRE, 1 security engineer | доказать рост производительности и независимость доменов на малом объёме |
| 4–7 мес. **Портал и первые миграции** | запустить catalog/search, query builder, семантический слой, export audit; перенести 10 приоритетных отчётов; внедрить onboarding-шаблон | портал MVP для 50 пилотных пользователей; p95 типового отчёта < 30 с; сверка на 100% ключевых KPI | Product Manager Portal, BI Lead, UX Lead, domain Data POs | 3 frontend/backend, 4 data, 2 BI, 1 UX, 1 QA/security; обучение бизнес-пользователей | ускорить управленческие решения и снять очередь на BI-команду |
| 7–10 мес. **Масштабирование и M&A** | подключить Corporate и Partners; онбордить одну фармацевтическую и одну medtech-компанию; ввести доменные квоты, chargeback, DR; заменить новые Camel-интеграции контрактами | 5+ доменов; новый партнёр за ≤ 6 недель; DR-тест RPO/RTO пройден | Integration Lead, Partner Domain PO, FinOps, SRE, Security | 2 integration, 3 domain/data на партнёра, 2 SRE, 1 FinOps | быстрее получить синергию от покупок и не раздувать DWH/ESB |
| 10–12 мес. **Переключение** | мигрировать оставшиеся целевые отчёты; заморозить новую логику в DWH/Power BI; перевести SQL Server в read-only; утвердить план вывода PowerBuilder/Camel | портал доступен всем целевым группам; бизнес-пользователи сами собирают отчёты; legacy больше не блокирует развитие | CTO, Transformation Lead, all Domain POs, Service Desk | migration factory: 6 data/BI, 2 change managers, 2 support, бюджет на dual-run | достичь годовой цели, снизить TCO и убрать блокирующий legacy |

## Сквозные потоки

- **Security & compliance:** threat model и data classification до пилота; MFA/ABAC, KMS, DLP, audit и residency — до первого production-набора.
- **Data governance:** owner, contract, lineage, retention и quality SLO — обязательный deployment gate.
- **SRE:** SLI/SLO, capacity, backup/restore, DR game day, runbooks и on-call развиваются вместе с платформой.
- **Change management:** ранние пилотные группы, champions в доменах, обучение и support-канал.
- **FinOps:** теги, budget alerts, квоты, showback и оптимизация compute/storage.

## Критерии go/no-go и rollback

| Gate | Go | No-go / rollback |
|---|---|---|
| Данные | 100% ключевых KPI совпадают; отклонение агрегатов в допуске | возврат чтения к legacy, блокировка новой версии продукта |
| Производительность | p95 типового отчёта < 30 с, error rate < 1%, нет кросс-доменной деградации | route трафика на предыдущую версию, снижение квот проблемного workload |
| Безопасность | нет critical/high; негативные ABAC-тесты пройдены; audit полон | отзыв доступа, разбор и повторный security review |
| Восстановление | restore/DR-тест укладывается в RPO/RTO | нет production-переключения до успешного game day |
| Принятие | ≥ 80% пилотной группы выполнили ключевые сценарии без помощи | расширить pilot/support; не выключать legacy UI |
