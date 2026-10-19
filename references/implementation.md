# Реализация и handoff: Figma / React / shadcn / Tilda

## A. Figma: системность до полировки

- Перед работой прочитай страницы Foundations, Tokens, Components и наиболее
  близкий существующий сценарий. Запиши source of truth; не угадывай.
- Ищи точное имя компонента, аналоги, variants, properties, nested slots.
  Отметь текущую и deprecated версии.
- Проверь `Instance → main component` и bindings на переменные. Если
  нужный компонент есть, используй его, а не создавай локальный близнец.
- Сценарии — обычные Frames; мастера — только в UI Kit. Следуй архитектуре
  Atoms → Molecules → Organisms, но не превращай любой контейнер в master.
- Layout: Auto Layout, Hug/Fill, адекватные constraints, text auto-resize,
  единый baseline, без случайного absolute (кроме overlay по смыслу).
- Состояния оформляй variants или отдельными страницами сценария.
- Сохраняй семантические имена слоёв, явную структуру и токен-обоснование.
- Проверяй реальные локализованные тексты и содержимое, не только Lorem Ipsum.
- Перед релизом проведи read-only `audit-design-system` (если доступен):
  detached, duplicates, raw styles, неверные variants и overrides.
- Новые компоненты создавай только после изучения библиотеки и согласования.

**Критерий:** другой дизайнер понимает происхождение любого повторно
использованного компонента и может менять его через опубликованный master.

## B. React / Tailwind / shadcn/ui

### Структура

- Сначала изучи проектные компоненты, theme, Tailwind config, CSS variables,
  typography, icon pack и роутинг. Не заменяй утверждённую тему собственным kit.
- semantic HTML: `button` для действий, `a` для переходов; реальные формы
  с `label`, `name`, `type`, error/help text и предсказуемой валидацией.
- Для UI используйте shadcn/ui/Radix в рамках проекта, не изобретай свои
  диалоги, selects и dropdown с отсутствующим keyboard handling.
- Layout: grid/flex с content-driven sizing, `min-width:0`, корректные
  overflow regions, sticky headers, предсказуемое место scroll.
- Состояния данных выражены явно: loading/error/empty/partial/success;
  ошибки не маскируются фиктивной успешной генерацией.
- Асинхронные операции должны поддерживать abort/cancel, где это реально,
  а внешние действия — confirmation + scope + server-side authorization.

### Доступность

- Keyboard order, видимый `:focus-visible`, accessible names, `aria-live`
  для значимых изменений без спама, диалог с focus trap + restoration.
- Контраст текста WCAG AA как разумный baseline (обычный текст 4.5:1,
  крупный 3:1); контраст важных UI границ/иконок не ниже 3:1, если применимо.
- Интерактивные target достаточного размера (ориентир 24 CSS px для AA,
  удобнее ~40–44 px для частых touch-сценариев, при соблюдении исключений).
- `prefers-reduced-motion` для animations и smooth scroll.
- `alt` достоверен; декоративные изображения — с пустым alt. Не придумывай,
  что изображено на фотографии.
- Проверка zoom 200%, длинной кириллицы, 320–390 px, клавиатуры и скролла.

### Performance / security

- Оптимизируй изображения (формат, dimensions, responsive sizes, lazy loading
  кроме главного LCP изображения), fonts preload выборочно, без CLS.
- Анимация преимущественно через transform/opacity, не бесконечно reflow.
- Не помещай ключи/токены в JS bundle, не полагайся на client-side permission
  check. Санитизация недоверенного HTML, защита форм и server-side validation.
- Не приписывай системе безопасность по одному визуальному осмотру.
- Моковые AI outputs явно помечай как демонстрационные и исключай из прода.

### Типовой паттерн для согласования AI action (псевдокод)

```tsx
// UI sketch, not drop-in production code. Реальные права проверяются на сервере.
function ConfirmAction({ preview, onConfirm, onCancel }) {
  return (
    <section aria-labelledby="action-review-title">
      <h2 id="action-review-title">Проверка перед отправкой</h2>
      <p>Эти изменения будут отправлены в систему после подтверждения.</p>
      <ChangeSummary data={preview} />
      <div className="flex gap-2">
        <Button variant="outline" onClick={onCancel}>Вернуться к редактированию</Button>
        <Button onClick={onConfirm}>Подтвердить отправку</Button>
      </div>
    </section>
  );
}
```

Здесь **нет** выдуманного server response или фиктивного `99% verified`.

## C. Tilda / статический сайт

- Сохрани реальную структуру Zero Block и адаптивов; кастомный JS нужен
  только для поведения, недостижимого штатными компонентами.
- Проверяй 390/768/1200+ px на каждой странице, особенно после смены
  языка и замены текстов.
- Формы: label, обязательные поля, маска и валидация номера по стране,
  feedback отправки/ошибки, anti-spam, настройка endpoint.
- Ссылки, хедер, footer, контакты, адрес, карта, `og:title`/`og:image`,
  canonical, favicon, link preview — часть QA, если сайт публикуется.
- i18n: непереводимые имена, согласованные словари, корректные названия
  города/улицы/бренда, независимые SEO поля для языковых версий.
- Выгрузку соцконтента проектируй как внешнюю интеграцию: TTL, удаление
  постов, fallback изображения, недоступность API и кеш обсуждаются явно.
- Security: не публиковать secret access tokens в клиенте; политики доступа
  и синхронизацию выполнять серверной стороной.

## D. Ширины и тестовая матрица

| Поверхность | Основные проверки |
|---|---|
| 360–390 | реальный mobile reflow; без горизонтального overflow |
| 768–834 | tablet columns, sidebar, navigation, controls |
| 1280–1440 | штатный desktop; реальный рабочий сценарий |
| 1920+ | max-width / column growth / таблицы / fixed sidebar |
| 200% zoom | тексты не обрезаны, цели доступны, важные controls видны |

Для B2B приложения дополнительно тестировать большое число выбранных chips,
состояние пустого списка, очень длинные ячейки, 2–3 уровня вложенности,
no permissions, offline/timeout, search typing и sticky pagination.

## E. Motion и GSAP

- Идея анимации формулируется как изменение состояния: что до/после и почему.
- Не анимируй layout свойства на горячем пути, если это не требуется.
- Убирай движения при reduced motion и остановке вкладки.
- GSAP cleanup при unmount и route changes; не дублируй ScrollTrigger.
- Векторные логотипы должны быть читаемы в каждой ключевой фазе движения:
  transition без «телепортации», easing с уместной массой, нет зависаний.

## F. Handoff contract

Передача содержит: контекст, сценарии, инварианты, Figma source, компоненты
(ссылки или IDs), tokens, API assumptions, state matrix, error copy,
responsive behavior, accessibility, animation, acceptance criteria,
known limits. Укажи что реально проверено, а что основано на допущениях.
