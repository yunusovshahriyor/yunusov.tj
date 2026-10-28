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
- `projects.ts` — карточки проектов. Данные (название, описание, категория, рейтинг, иконка, баннер) взяты со страницы разработчика в Google Play: `https://play.google.com/store/apps/dev?id=8979338274923782952`. Иконки и баннеры скачаны в `public/projects/`. Поле `role` указано как «Разработчик» для всех — при необходимости уточните формулировку.
- `services.ts` — блок «Услуги».
- `process.ts` — этапы работы.
- `technologies.ts` — категории технологий. Добавляйте инструменты в массив `items` только те, которыми реально владеете.
- `blogTopics.ts` — темы будущего блога.

Фото для раздела «Обо мне» — временный плейсхолдер (`src/components/ui/ImagePlaceholder.tsx`, компонент `PhotoPlaceholder`). Замените его на реальную фотографию через `next/image`, когда она будет готова.

Если появятся новые приложения в Google Play, добавьте их в `projects.ts` по той же схеме (скачайте иконку `=s256-rw` и баннер `=w1052-h592-rw` с `play-lh.googleusercontent.com` в `public/projects/`).

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

## Тестовый деплой на GitHub Pages

В репозитории настроен workflow `.github/workflows/deploy-pages.yml`, который при пуше в ветку `claude/clever-cori-8bobpv` собирает сайт как статический экспорт и публикует его на GitHub Pages.

**Разовая настройка (один раз в самом репозитории на GitHub):**

1. Зайдите в **Settings → Pages**.
2. В блоке «Build and deployment» → **Source** выберите **GitHub Actions**.
3. Сделайте любой пуш в ветку `claude/clever-cori-8bobpv` (или запустите workflow вручную во вкладке **Actions**) — сайт появится по адресу `https://<ваш-github-username>.github.io/yunusov.tj/`.

**Важно про этот тестовый режим:**

- GitHub Pages отдаёт только статические файлы и не может выполнять серверный код, поэтому маршрут `/api/contact` (отправка заявок в Telegram) в этой сборке исключается автоматически.
- Форма заявок в этом режиме вместо отправки на сервер открывает у пользователя почтовый клиент с письмом на адрес из `src/data/contacts.ts` (`contacts.email`).
- Для финальной публикации на постоянном хостинге (Vercel, Railway и т. д.) эти ограничения не действуют — там форма и API-маршрут работают как обычно.
- Когда переедете на постоянный домен, поменяйте триггер workflow (`on.push.branches`) на вашу основную ветку (например, `main`) или просто удалите файл workflow, если статический тест на Pages больше не нужен.

## Telegram SMM-бот

Дар папкаи `telegram-bot/` боти Telegram ҷойгир аст: обуначӣ дар шарҳҳои канал калимаи рамзӣ менависад ва бот ссилкаро ба директ мефиристад. Он аз сайт мустақил аст ва алоҳида (масалан, дар Railway бо Root Directory `telegram-bot`) ба кор андохта мешавад. Дастур — `telegram-bot/README.md`.
