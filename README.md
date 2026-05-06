# Fruit Story POS Starter

This repo is a deployment-ready starter around the current Fruit Story POS checkpoint.

## What is included

- `index.html` contains the current working single-file POS checkpoint.
- `src/config` contains Firebase config and database paths.
- `src/services` contains starter service wrappers for orders, products, chat, billing, and Firebase DB operations.
- `firebase/database.rules.json` contains starter Realtime Database rules.
- `firebase/seed.json` contains initial settings, roles, billing, and chat channel data.
- `api/gemini-scan.js` is a server-side placeholder for private AI scan calls.

## Local setup

```bash
npm install
cp .env.example .env.local
npm run dev
```

## Deployment

1. Push this folder to GitHub.
2. Import the repo into Vercel.
3. Add environment variables from `.env.example` to Vercel.
4. Run `npm run build` or let Vercel build automatically.

## Firebase migration order

1. settings
2. users / roles
3. products
4. orders
5. inventoryLogs
6. kitchen / delivery / pickup status fields
7. billing
8. chat
9. activityLogs

## Production notes

- Move the inline POS code from `index.html` into `src/modules` one module at a time.
- Do not keep private API keys in browser code.
- Use Firebase Auth before enforcing the role-based security rules.
