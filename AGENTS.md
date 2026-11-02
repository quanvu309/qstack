qstack is a set of agent skills for writing and designing in Vietnamese. Skills live in bucket folders under `skills/`:

- `writing/`: Vietnamese prose, UI copy, and the project voice
- `design/`: typography, layout, and locale data for Vietnamese users
- `in-progress/`: beta, public on purpose, not shipped in the plugin
- `deprecated/`: no longer used

`writing/` and `design/` are the **promoted** buckets. Create the other two only when a skill needs one.

Run `node scripts/check.mjs` after every change. It enforces the structural rules: frontmatter `name` equals the folder name, each skill has `agents/openai.yaml` whose `policy.allow_implicit_invocation: false` matches `disable-model-invocation: true`, every promoted skill (and only those) is listed in `.claude-plugin/plugin.json` and linked from the top-level `README.md`, every skill is linked from its bucket `README.md`, relative links resolve, text is Unicode NFC, and no file contains the long dash (U+2014). Run `claude plugin validate . --strict` after touching either file in `.claude-plugin/`.

## Writing skills here

Write every `SKILL.md` with the `writing-for-agents` skill from [mattpocock/skills](https://github.com/mattpocock/skills). A skill is either **model-invoked** (a model-facing description carrying its trigger branches, including the Vietnamese words users type) or **user-invoked** (`disable-model-invocation: true`, a one-line human-facing description). One skill reaches another by an instruction to call the Skill tool with its name, never by linking into another skill's folder.

Language split:

- Skill bodies, reference files and this file are English, because agents follow English instructions most predictably. Every example of Vietnamese text inside them is Vietnamese.
- `README.md`, bucket `README.md`s and `CONTRIBUTING.md` are Vietnamese, because they are for the people who use the skills.
- Vietnamese text in this repo follows `skills/writing/vietnamese-writing`, the same rules the skills teach.

A fact about Vietnam that can change (administrative units, phone formats, laws, font support) carries its source and the date it was checked, in the same sentence. Every Vietnamese example must read as native to a native speaker; a skill that teaches translationese with translationese examples teaches the wrong thing.

## Grouping in READMEs

Bucket `README.md`s and the top-level `README.md` group promoted skills under **Gọi tay** (user-invoked) and **Agent tự gọi** (model-invoked). Each entry links the skill name to its `SKILL.md` and gives one line on what it does.

## Releases

Bump `version` in `.claude-plugin/plugin.json` when a skill's behaviour changes, and add a line to `CHANGELOG.md`. Installed plugins update only when that version changes.

To link every skill outside `deprecated/` into `~/.claude/skills` and `~/.agents/skills` for local testing, run `scripts/link-skills.sh`.
