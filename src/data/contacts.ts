// Замените placeholder-значения на реальные ссылки и email перед публикацией сайта.
export const contacts = {
  telegram: {
    label: "Telegram",
    href: "https://t.me/your_username",
  },
  instagram: {
    label: "Instagram",
    href: "https://instagram.com/your_username",
  },
  youtube: {
    label: "YouTube",
    href: "https://youtube.com/@your_channel",
  },
  email: {
    label: "hello@yunusov.tj",
    href: "mailto:hello@yunusov.tj",
  },
};

export type ContactKey = keyof typeof contacts;
