# Changelog

## 0.0.3

- Skills renamed with a short `vi-` prefix: `vietnamese-writing` → `vi-writing`, `setup-qstack` → `vi-setup`, `vietnamese-official-document` → `vi-official-doc`, `vietnamese-one-pager` → `vi-one-pager`, `vietnamese-typography` → `vi-typography`, `vietnamese-locale` → `vi-locale`. Run `/vi-setup` where you ran `/setup-qstack`.
- New `documents/` bucket holds `vi-official-doc` and `vi-one-pager`.
- The READMEs and CONTRIBUTING are rewritten with `vi-writing`, in the project voice now recorded in `AGENTS.md`.

## 0.0.2

- New skill `vietnamese-one-pager`: one-page tờ trình, updates and proposals, answer first, with a page budget measured by rendering and phụ lục that can be added later.
- The `.docx` builder renders `appendices` (Phụ lục I, II... on new pages with their own page numbers) and `table` blocks, and no longer spills a blank second page when the signature ends near the bottom of page 1.
- `build_docx.py --one-page` refuses a main page over 275 chữ and prints the count otherwise.
- Kính gửi now comes before the căn cứ lines in a tờ trình or báo cáo.
- The README shows rendered example documents, attached to each GitHub release by `scripts/release.sh`.

## 0.0.1

- First release: `vietnamese-writing`, `setup-qstack`, `vietnamese-typography`, `vietnamese-locale`.
- `vietnamese-official-document`: văn phong hành chính for government and corporate documents, the Nghị định 30/2020 layout, and a `.docx` builder. `vietnamese-writing` routes official documents to it.
