# Instagram «Comment → DM» бот

Вақте зери Reels калимаи рамз менависанд (`ДАВР`, `КОД`, `ШАРТ`, `РӮЙХАТ`, `ТАҒЙИРЁБАНДА`),
бот ба муаллифи шарҳ дар Direct пайванди канали Telegram мефиристад ва ба худи шарҳ
кӯтоҳ ҷавоб медиҳад: «📩 Ба Direct фиристодам!». Ба як нафар зери як ролик танҳо як бор менависад.

Бот дар **Cloudflare Workers** кор мекунад (ройгон) ва **Instagram API with Instagram Login**-ро
истифода мебарад (Private Replies: ба ҳар шарҳ як паём, дар давоми 7 рӯз).

Файлҳо: `worker.js` — худи бот (як файл, бе вобастагӣ), `test.mjs` — санҷиш (`node test.mjs`).

## Қадамҳо

### 1. Worker дар Cloudflare
1. dash.cloudflare.com → **Workers & Pages** → **Create** → **Create Worker** → ном: `ig-dm-bot` → **Deploy**.
2. **Edit code** → тамоми матни `worker.js`-ро гузоред → **Deploy**.
3. Суроғаи Worker-ро нусха кунед: `https://ig-dm-bot.<номи-шумо>.workers.dev`.

### 2. Хотираи KV (то ду бор нафиристад)
1. **Storage & Databases → KV → Create** → ном: `ig_dm_bot`.
2. Worker → **Settings → Bindings → Add → KV namespace** → Variable name: `SEEN`, namespace: `ig_dm_bot`.

### 3. Барномаи Meta
1. developers.facebook.com → **My Apps → Create App** → ҳолати истифода: **«Manage messaging & content on Instagram»**.
2. **Instagram → API setup with Instagram login**:
   - **Generate access tokens** → акаунти `shahriyor_yunusov`-ро илова кунед → токенро нусха кунед.
   - **Instagram app secret**-ро нусха кунед.
   - Иҷозатҳо: `instagram_business_basic`, `instagram_business_manage_comments`, `instagram_business_manage_messages`.
3. Дар Instagram: Настройки → Сообщения → **«Разрешить доступ к сообщениям»** (Connected tools) — фаъол.

### 4. Тағйирёбандаҳои Worker
Worker → **Settings → Variables and Secrets → Add**:
| Ном | Навъ | Қимат |
|---|---|---|
| `IG_ACCESS_TOKEN` | Secret | токен аз қадами 3 |
| `IG_APP_SECRET` | Secret | Instagram app secret |
| `VERIFY_TOKEN` | Secret | ҳар матни тасодуфӣ, масалан `davr-2026-xyz` |
| `TELEGRAM_LINK` | Text | пайванди канал, масалан `https://t.me/...` |
| `KEYWORDS` | Text, ихтиёрӣ | JSON: `{"ДАВР": "Салом! Шпаргалка 👉 {link}"}` |

### 5. Webhook
Дар барномаи Meta → **Instagram → API setup → Configure webhooks**:
- **Callback URL:** суроғаи Worker
- **Verify token:** ҳамон `VERIFY_TOKEN`
- **Verify and save** → обуна ба майдони **`comments`**.

### 6. Санҷиш ва Live
- Дар ҳолати **Development** Meta вебхукҳоро танҳо барои корбароне мефиристад, ки дар барнома нақш доранд
  (админ, тестер). Бо акаунти дигари худ (тестер) зери ролик «ДАВР» нависед ва санҷед.
- Барои ҳамаи обуначиён барнома бояд **Live** бошад ва иҷозатҳои `instagram_business_manage_comments`
  ва `instagram_business_manage_messages` **Advanced Access** гиранд (App Review дар Meta).
  Барои ин Meta видеои кӯтоҳи кори бот ва сиёсати махфият (Privacy Policy URL) мехоҳад.

### Логҳо
Worker → **Logs** (Real-time): `dm <comment_id> <калима> <status>` ва хатоҳои Graph API.

### Токен
Токени Instagram ~60 рӯз эътибор дорад. Пеш аз анҷом онро дар барномаи Meta нав кунед
ва дар `IG_ACCESS_TOKEN` иваз кунед.
