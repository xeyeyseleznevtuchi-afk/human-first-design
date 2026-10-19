# Источники и происхождение подхода

## Первичный источник AI UX

Taras Bakusevych / Syntax Stream —
[39 Principles for Designing Human–AI Interaction](https://syntaxstream.substack.com/p/42-principles-for-designing-humanai),
30.06.2026. На момент подготовки (19.10.2026) опубликованная версия
насчитывает **39**, хотя адрес исторически содержит «42».

Материал описывает 9 кластеров: вероятностность, ожидания, доверие,
прозрачность, контроль, управляемый сбой, совместная работа,
ответственная автономность, доверие во времени. Наш `human-ai-39.md`
— оригинальное практическое изложение с собственными UX-правилами и тестами.
Дизайн чужих иллюстраций и тексты статьи не включены в поставку.

Указанные в статье смежные источники:
- [Microsoft: Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
- [Google PAIR Guidebook](https://pair.withgoogle.com/guidebook/)
- [OpenAI Model Spec](https://model-spec.openai.com/)
- [Anthropic Constitution](https://www.anthropic.com/constitution)
- [Eric Horvitz: mixed-initiative UI](https://erichorvitz.com/)

## Visual taste / frontend

- [Anthropic Claude Code — Frontend Design (original SKILL.md)](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md).
  Взят подход art direction based on subject matter, deliberate hierarchy,
  typography, copy, restraint, self-critique и screenshot QA.
- [Leonxlnx / Taste Skill, design-taste-frontend](https://github.com/Leonxlnx/taste-skill).
  Взяты концепции антишаблонного дизайна, переключаемых уровней variance,
  motion, density, audit-first редизайна и preflight-check; **не** скопированы
  сторонние реализации, генераторы, готовые стилевые системы или скрипты.
  Taste Skill v2.1 описывает отдельный маршрут для app/dashboard; стандартный v2
  делает акцент на арт-дирекции и реальном браузерном QA, а не трёх ручках.
  Наш `references/taste-v2-process.md` — самостоятельная операционализация по
  опубликованному README, а не буквальная интеграция кода/скриптов v2.1.

## Локальные наработки из прежних дизайн-проектов

- `audit-design-system.md` — доступный read-only пользовательский скилл:
  drift, detached instances, raw styles, variant mismatch, evidence/impact.
  В `human-first-design` предусмотрена интеграция при наличии исходного файла.
- Из ранее обсуждавшейся практики `human-first-web-audit` учтены clarity,
  trust, human feeling, conversion, honest limitations. Сам оригинальный
  **SKILL.md в доступных файлах не найден**, поэтому он не заявлен как
  объединённый дословно.
- Предпочтения к product design: UI Kit-first, reuse вместо локальных копий,
  Figma Auto Layout, реальные RU/EN строки, проверка переполнений и соседних
  состояний, корректная локализация имён собственных.

## Ограничения

Это сборный, адаптированный рабочий скилл для Claude Code и других агентов,
понимающих `SKILL.md`, а не официальный выпуск Anthropic, Google, Microsoft,
Syntax Stream или Taste Skill. Принципы не гарантируют юридическое соответствие,
безопасность backend или достоверность AI без реальных тестов.
