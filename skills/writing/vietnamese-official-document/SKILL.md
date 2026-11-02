---
name: vietnamese-official-document
description: Draft and build Vietnamese official documents (văn bản hành chính) in government or corporate tone and the Nghị định 30/2020 layout. Use for quyết định, công văn, tờ trình, thông báo, báo cáo, kế hoạch, biên bản, giấy mời, giấy giới thiệu, or when asked for a .docx in that format.
---

# Vietnamese official document

An official document is judged on two things a reader sees at once: whether it sounds like an office wrote it (**văn phong hành chính**) and whether the page looks like the decree's template (**thể thức**). Do both, in this order.

## 1. Pick the type and its skeleton

Choose the type from the reader's purpose, then open that type's section in [TYPES.md](TYPES.md) and follow its skeleton block by block:

| Purpose | Type |
| --- | --- |
| Decide, appoint, approve, issue a rule | Quyết định |
| Ask, answer, or inform another organisation | Công văn |
| Propose to a superior for approval | Tờ trình |
| Announce to many people | Thông báo |
| Report results to a superior | Báo cáo |
| Set out what will be done, by whom, by when | Kế hoạch |
| Record a meeting or an event | Biên bản |
| Invite to a meeting or event | Giấy mời |
| Introduce a person sent to work with another organisation | Giấy giới thiệu |

## 2. Write in văn phong hành chính

Văn phong hành chính is impersonal, exact, standard and courteous. Every sentence must survive being read aloud in a meeting and quoted in a dispute.

**Voice.** The issuing organisation speaks in the third person by its name or short name ("Công ty", "Sở Tài chính", "Ban Giám đốc"). The recipient is "Quý cơ quan", "Quý Công ty", "Quý khách hàng", or the organisation's name. Personal pronouns (tôi, chúng tôi, bạn, mình) have no place in the body.

**Courtesy by direction.** The verb carries the rank:

| Writing to | Ask with | Example |
| --- | --- | --- |
| A superior body | kính trình, kính đề nghị | "Công ty kính trình Hội đồng quản trị xem xét, phê duyệt." |
| A peer or partner | đề nghị, trân trọng đề nghị | "Công ty trân trọng đề nghị Quý Công ty phối hợp cung cấp hồ sơ." |
| A subordinate unit | yêu cầu, giao | "Giao Phòng Kế toán chủ trì, hoàn thành trước ngày 15/11/2026." |

**Exactness.** Name the actor, the action, the object, the deadline and the unit in charge in every instruction: "Phòng Hành chính - Nhân sự chủ trì, phối hợp với Phòng Kế toán hoàn thành việc rà soát hồ sơ trước ngày 30/11/2026." One sentence carries one obligation. Money appears in digits, then in words: "50.000.000 đồng (Năm mươi triệu đồng)". A cited document appears in full on first mention: type, number, date, issuing body, title ("Luật Doanh nghiệp số 59/2020/QH14 ngày 17 tháng 6 năm 2020 của Quốc hội"). An abbreviation appears after its full name in parentheses on first use, then alone. A fact the user did not give (a cost breakdown, an account number, a contract clause, a phone number) stays a visible placeholder in brackets, "[số tài khoản]", and you list the placeholders after the document; an invented figure in a signed document is a liability. Lists inside a khoản are lettered in the Vietnamese alphabet: a), b), c), d), đ), e), g), h), i), k).

**Standard formulas.** Use the decree-era phrases readers expect, verbatim:

- Basis: "Căn cứ...;", "Theo đề nghị của...", "Xét đề nghị của..." (Quyết định), "Thực hiện..." (Công văn, Kế hoạch, Báo cáo).
- Purpose opener: "Nhằm...", "Để...".
- Request: "đề nghị Quý cơ quan xem xét, giải quyết", "kính trình... xem xét, phê duyệt".
- Effect and execution: "Quyết định này có hiệu lực kể từ ngày ký.", "... chịu trách nhiệm thi hành Quyết định này./."
- Closing a công văn: "Trân trọng cảm ơn sự phối hợp của Quý cơ quan./." or "Trân trọng./." (convention; the decree prescribes none).
- End marker: the last body line ends with "/." right after its period, as every template in the decree shows.

A document closes once. "Kính trình... xem xét, phê duyệt./." ends a tờ trình by itself; adding "Trân trọng./." after it is a second closing.

**Register.** Hán Việt is the norm here (thực hiện, triển khai, phối hợp, chủ trì). Keep it plain: no metaphor, no emotive adjective, no exclamation mark, no rhetorical question, no hedge ("có lẽ", "khá"). Feeling becomes a fact or goes: "kết quả đáng tự hào" becomes "doanh thu đạt 112% kế hoạch năm".

**Government and corporate.** A state body writes to citizens and lower bodies with "cơ quan, tổ chức, cá nhân có liên quan" and cites legal grounds for every decision. A company follows the same layout, cites its charter (Điều lệ) and internal rules as grounds, and addresses customers and partners as "Quý khách hàng", "Quý đối tác". Nghị định 30/2020 binds state bodies; companies follow it by convention, so match it unless the company has its own template.

## 3. Run the translationese catalog

Call the Skill tool with "vietnamese-writing" and check every sentence of the draft against its translationese catalog. Its register advice (thuần Việt over Hán Việt) does not apply here; every catalog pattern does. This step is done when you have rewritten each sentence a pattern caught, or confirmed none did.

## 4. Deliver

**Text.** Output the whole page in reading order: the header as two columns (issuer name and Số on the left; "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc" and the date on the right), the title block, the body, then Nơi nhận beside the signer block. The Quốc hiệu and Tiêu ngữ appear on every type.

**File.** Write a JSON spec and build a `.docx` with the layout from [FORMAT.md](FORMAT.md):

```bash
uv run --with python-docx <skill-dir>/scripts/build_docx.py spec.json out.docx
```

`<skill-dir>` is the absolute path of the folder holding this SKILL.md. `--help` prints the spec fields and the type codes, and `examples/` holds a full spec for a quyết định, a công văn and a biên bản. The script refuses a spec with a missing required field and names the field. A spec may carry `appendices` (each a phụ lục on its own pages) and `{"table": [[...], ...]}` body blocks; `--one-page` refuses a main page over 275 chữ.

Either way, leave the number and the day blank in a draft: the clerk (văn thư) assigns both at issuance. In a spec, omit `number` and give `date` as year and month.

## Done when

Every block of the type's skeleton in TYPES.md is present in order, the header carries the Quốc hiệu and Tiêu ngữ, every fact traces to the user or a placeholder, every instruction names actor, action, deadline and unit in charge, no personal pronoun appears in the body, every cited document is in full form on first mention, step 3 is done, and, when a file was asked for, the script built it without error.
