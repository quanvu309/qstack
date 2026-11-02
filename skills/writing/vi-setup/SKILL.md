---
name: vi-setup
description: Set this project's Vietnamese voice once (xưng hô, register, spelling, money and date forms) so every qstack skill writes the same way.
disable-model-invocation: true
---

# Set up qstack

Record the project's Vietnamese voice as a `## Vietnamese voice` section in the repo's `AGENTS.md` (or `CLAUDE.md` when the repo has only that). The qstack skills read that section and follow it over their own defaults. These are brand calls, so the user decides each one; your job is to make each decision quick.

## 1. Look before asking

Read any existing Vietnamese copy in the repo: locale files (`vi.json`, `messages/vi.*`, `*.po`), landing pages, emails. Note which address pair, tone mark style and currency form it already uses, and whether it mixes them. A pre-existing voice section means this run edits it.

## 2. Ask in one round

Ask every question below in a single message, numbered, each with your recommended answer drawn from step 1 and a one-line example sentence for each option:

1. **Address pair** (cặp xưng hô): no pronoun, chúng tôi / bạn, mình / bạn, chúng tôi / quý khách, em / anh or chị, or a custom pair.
2. **Register**: plain thuần Việt, or formal with Hán Việt.
3. **Spelling**: old tone style with y (hòa, thủy, kỹ), or the textbook standard of new style with i (hoà, thuỷ, kĩ). Education products take the textbook standard.
4. **Loanwords**: which English terms the audience says aloud and should stay English (email, app, deploy...).
5. **Money and dates**: đ, ₫, or VND; 2/11/2026 or 02/11/2026; 14:30 or 14h30.
6. **Regional vocabulary**: national, Northern, or Southern.

Where step 1 found mixed usage, show both forms with file paths so the user sees the cost of each choice.

## 3. Write the section

Write the answers as short declarative lines under `## Vietnamese voice`, each with one example sentence in that voice. Keep it under 15 lines: it loads on every turn.

Done when the section exists in the file, every one of the six answers is in it, and you have shown the user the final text.
