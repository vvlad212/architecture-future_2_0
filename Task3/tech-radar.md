# Технологический радар

Кольца: **Adopt** — стандарт для production; **Trial** — пилот на ограниченном домене; **Assess** («Asset» в материале курса) — прототип и оценка; **Hold** — не использовать в новых решениях, подготовить вывод.

Тренды: ↑ движется к Adopt; → остаётся; ↓ движется к Hold.

| ID | Квадрант | Технология / подход | Кольцо | Тренд | Какой бизнес-сценарий поддерживает |
|---:|---|---|---|:---:|---|
| 1 | Платформы | Облачная landing zone, VPC, IAM, KMS, Object Storage | Adopt | ↑ | быстрое масштабирование, изоляция доменов, снижение CAPEX |
| 2 | Инструменты | Terraform + удалённый state + policy-as-code | Adopt | ↑ | воспроизводимые среды, быстрый onboarding новых направлений |
| 3 | Методы | GitOps, CI/CD, ADR, threat modeling | Adopt | ↑ | короткий lead time при контролируемом риске |
| 4 | Методы | Data contracts и domain ownership | Adopt | ↑ | независимое развитие финтеха, клиник и партнёров |
| 5 | Инструменты | OIDC, MFA, RBAC + ABAC, audit trail | Adopt | ↑ | самообслуживание в границах допуска и регуляторная трассируемость |
| 6 | Языки/фреймворки | Python для data/AI, Go/Java для сервисов | Adopt | → | повторное использование текущих компетенций |
| 7 | Платформы | Kubernetes / Managed Kubernetes | Trial | ↑ | независимое масштабирование портала, ingestion и доменных сервисов |
| 8 | Платформы | Kafka / managed event streaming + Schema Registry | Trial | ↑ | слабая связность доменов и near-real-time финтех-отчёты |
| 9 | Платформы | Lakehouse: S3-compatible storage + Apache Iceberg | Trial | ↑ | сотни ТБ, история и schema evolution без монолитного DWH |
| 10 | Инструменты | Trino / distributed SQL | Trial | ↑ | параллельные ad-hoc отчёты и разделение compute/storage |
| 11 | Инструменты | dbt + Airflow/Dagster | Trial | ↑ | версионируемые трансформации, тесты и lineage; ускорение отчётности |
| 12 | Инструменты | OpenMetadata/DataHub + Great Expectations/Soda | Trial | ↑ | поиск наборов, ответственность, lineage и доверие к KPI |
| 13 | Инструменты | OpenTelemetry + метрики data SLO | Trial | ↑ | раннее обнаружение деградации качества/свежести |
| 14 | Методы | Data Mesh для двух пилотных доменов | Trial | ↑ | проверка независимого владения без big-bang-реорганизации |
| 15 | Платформы | Apache Flink / streaming SQL | Assess | ↑ | потоковый risk/fraud и оперативные KPI, если Kafka + batch не дают нужную freshness |
| 16 | Платформы | Serverless query/ETL | Assess | → | нерегулярные нагрузки новых партнёров без резерва compute |
| 17 | Инструменты | Data virtualization | Assess | → | временный доступ к legacy во время миграции |
| 18 | Методы | FinOps showback/chargeback по доменам | Assess | ↑ | прозрачная стоимость отчётов и контроль облачных затрат |
| 19 | Платформы | SQL Server 2008 как целевое DWH | Hold | ↓ | только read-only legacy до завершения сверки и миграции |
| 20 | Языки/фреймворки | PowerBuilder для нового UI | Hold | ↓ | замена на web-портал снижает lead time и дефицит кадров |
| 21 | Методы | Бизнес-логика в DWH, shared database | Hold | ↓ | устранение междодоменных блокировок и регрессий |
| 22 | Инструменты | Point-to-point-трансформации в Camel ESB | Hold | ↓ | новые компании подключаются как домены через типовой contract |
| 23 | Инструменты | Бизнес-логика в кастомном Power BI | Hold | ↓ | семантика и трансформации переносятся в код и единый semantic layer |

## Правила движения

- Assess → Trial: есть ADR, owner, угроза-модель, стоимостная оценка и прототип с измеримым эффектом.
- Trial → Adopt: пилот прошёл SLO, security, DR, load и operability-проверки; есть runbook и обученная команда.
- Любое кольцо → Hold: риск/стоимость превысили ценность, нет владельца или есть поддерживаемая замена.
- Радар пересматривается квартально Architecture Council; владелец каждого Trial даёт метрики до заседания.
