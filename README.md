# Shahriyor Yunusov — персональный сайт

Личный сайт-портфолио программиста и IT-фрилансера Shahriyor Yunusov. Next.js (App Router) + TypeScript + Tailwind CSS.

## Разработка

```bash
npm install
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000).

```bash
npm run build   # production-сборка
npm run start   # запуск production-сборки
npm run lint    # проверка ESLint
```

## Структура контента

Весь текстовый контент вынесен в `src/data/*.ts`, чтобы его можно было менять без правки компонентов:

- `site.ts` — название, домен, title/description для SEO.
- `contacts.ts` — ссылки на Telegram, Instagram, YouTube и email. **Замените placeholder-ссылки на реальные перед публикацией.**
- `projects.ts` — карточки проектов (ZabonDon, Markazi Khirad, Kitobkhonai Millioner). Поля вроде `role`, `technologies` и `link` содержат `[Добавить ...]` — заполните реальными данными по мере готовности.
- `services.ts` — блок «Услуги».
- `process.ts` — этапы работы.
- `technologies.ts` — категории технологий. Добавляйте инструменты в массив `items` только те, которыми реально владеете.
- `blogTopics.ts` — темы будущего блога.

Фото и скриншоты проектов — временные плейсхолдеры (`src/components/ui/ImagePlaceholder.tsx`). Замените их на реальные изображения через `next/image`, когда материалы будут готовы.

## Форма заявок

Форма на странице отправляет `POST /api/contact` (`src/app/api/contact/route.ts`). Чтобы заявки приходили в Telegram, задайте переменные окружения:

```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

Без них заявки просто логируются на сервере — добавьте нужную интеграцию (email-сервис, CRM и т. д.) при необходимости.

## SEO

- Метаданные и Open Graph — `src/app/layout.tsx`.
- `sitemap.xml` и `robots.txt` генерируются автоматически (`src/app/sitemap.ts`, `src/app/robots.ts`).
- Домен для метаданных задаётся в `src/data/site.ts` (`url`) — обновите его перед публикацией на реальном домене.
