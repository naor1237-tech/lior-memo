# 42 התוספים ל-Claude Code: מה מותקן בפרויקט הזה

נוסף ב-23.11.2026 (נאור: "תוסיף הכל לכל הפרויקטים"), לפי המדריך "42 תוספים ל-Claude Code".
אותו קובץ ואותן הגדרות בכל 8 הפרויקטים. כללי CLAUDE.md של הפרויקט גוברים על כל תוסף.

## 1. פלאגינים (`.claude/settings.json`: `extraKnownMarketplaces` + `enabledPlugins`)
Claude Code מתקין אותם לבד כשפותחים את הפרויקט ומאשרים אותו (או `/plugin` ← install). אחרי שינוי: `/reload-plugins`.

| # | כלי | פלאגין |
|---|---|---|
| 01 | Superpowers | `superpowers@claude-plugins-official` |
| 05 | Vercel | `vercel@claude-plugins-official` (צריך חשבון) |
| 06 | Playwright | `playwright@claude-plugins-official` |
| 07 | Codex | `codex@openai-codex` (צריך חשבון OpenAI) |
| 08 | Claude HUD | `claude-hud@claude-hud` |
| 09 | Figma | `figma@claude-plugins-official` (צריך חשבון) |
| 10 | ui-ux-pro-max | `ui-ux-pro-max@ui-ux-pro-max-skill` |
| 11 | impeccable | `impeccable@impeccable` |
| 12 | taste-skill | `taste-skill@taste-skill` |
| 14 | HyperFrames | `hyperframes@claude-plugins-official` |
| 17 | Higgsfield | `higgsfield@higgsfield` (צריך חשבון + `higgsfield auth login`) |
| 18 | Perplexity | `perplexity@perplexity-mcp-server` (צריך מפתח API) |
| 20 | Firecrawl | `firecrawl@claude-plugins-official` (צריך חשבון) |
| 22 | last30days | `last30days@last30days-skill` |
| 24 | humanizer | `humanizer@humanizer` (באנגלית; בעברית עדיף `hebrew-ai-text-humanizer`) |
| 37 | Slack | `slack@claude-plugins-official` |
| 38 | Zapier | `zapier@claude-plugins-official` (צריך חשבון) |
| 39 | caveman | `caveman@caveman`, **רשום אבל כבוי** |

**למה caveman כבוי:** הוא נדלק בכל תחילת סשן (hook של SessionStart) ומקצר את כל התשובות לסגנון "איש מערות". זה סותר את הכלל "חם, ישיר, מקצועי" ואת התשובות בעברית מלאה. להדלקה: `"caveman@caveman": true` ב-`.claude/settings.json`.

## 2. שרתי MCP (`.mcp.json`)
בפעם הראשונה Claude Code שואל אם לאשר אותם, ואז `/mcp` ← התחברות לחשבון.

| # | כלי | חיבור |
|---|---|---|
| 21 | Apify | `https://mcp.apify.com` |
| 25 | Metricool | `https://ai.metricool.com/mcp` |
| 27 | Nano Banana | `uvx nanobanana-mcp-server@latest` עם `GEMINI_API_KEY` מהסביבה (פרויקט קהילתי) |
| 28 | ElevenLabs | `https://api.elevenlabs.io/v1/mcp` |
| 31 | Granola | `https://mcp.granola.ai/mcp` |
| 34 | Notion | `https://mcp.notion.com/mcp` |

## 3. סקילים בתוך הפרויקט (`.claude/skills/`)
| # | כלי | מקור | רישיון |
|---|---|---|---|
| 13 | emil-design-eng ועוד 19 סקילים של אנימציה ועיצוב | github.com/emilkowalski/skills @ 64eb3de | MIT |
| 15 | Remotion (13 סקילים, `remotion-*`) | github.com/remotion-dev/skills @ 89c8afa | אין קובץ רישיון במאגר; Remotion עצמו דורש רישיון חברה לעסק עם יותר מ-3 עובדים (ראו הסקיל `remotion-license`) |
| 40 | find-skills | github.com/vercel-labs/skills @ 57217cf | MIT |

## 4. מה לא נכנס לקבצי הפרויקט, ולמה
| # | כלי | איפה |
|---|---|---|
| 02 | gstack | ‎128MB, מותקן ב-`~/.claude/skills/gstack` (סקריפט הסביבה, או ידנית לפי המדריך) |
| 03 | graphify | `pip install graphifyy && graphify install` |
| 04 | GitHub CLI | `brew install gh` במק; בענן GitHub מחובר דרך MCP |
| 16 | ffmpeg | `brew install ffmpeg` / `apt-get install ffmpeg` |
| 19 | Claude in Chrome | תוסף לדפדפן במחשב, ואז `claude --chrome` |
| 23 | Gemini CLI | `npm install -g @google/gemini-cli` |
| 26 | GPT Image | צריך מפתח OpenAI ובנייה מהמקור (github.com/SureScaleAI/openai-gpt-image-mcp); נוסיף כשיהיה מפתח |
| 29 | Puppeteer | `npm i puppeteer` רק בפרויקט שצריך אותו |
| 30, 35, 36 | Google Drive, Gmail, Calendar | connectors ב-claude.ai/customize/connectors (כבר מחוברים) |
| 32 | Whisper | `pip install -U openai-whisper` |
| 33, 41 | Python, Node.js | התקנה במחשב |
| 42 | Ollama | `curl -fsSL https://ollama.com/install.sh \| sh` במחשב |

## אבטחה
פלאגינים וסקילים של צד שלישי מריצים קוד ו-hooks. לא מריצים סקריפטים מתוך סקיל שנוגעים בתשלומים, SMS, וואטסאפ או פריסה בלי אישור של נאור. מפתחות API לא נכתבים ב-`.mcp.json`; רק `${משתנה}` מהסביבה.
