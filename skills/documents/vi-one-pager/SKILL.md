---
name: vi-one-pager
description: Write a Vietnamese one-pager, a tờ trình, progress update or proposal that a reader can decide from on one page, with the detail moved into phụ lục that can be added later. Use when asked for a one-pager, tóm tắt một trang, tờ trình ngắn, báo cáo nhanh, cập nhật tiến độ, or đề xuất, when cutting a long document down to one page, or when adding a phụ lục to one.
---

# Vietnamese one-pager

A one-pager serves two readers. The **decider** reads only the page and must be able to act on it. The **checker** opens the phụ lục to verify the numbers. Write the page **answer first**: the ask or the status comes in the first sentence, and everything after it supports that sentence.

## 1. Write the lead sentence

Before anything else, write the one sentence the reader acts on.

- Proposal: "Phòng Hành chính - Nhân sự kính trình Giám đốc phê duyệt kinh phí 85.000.000 đồng tổ chức khóa đào tạo kỹ năng quản lý cho 20 trưởng nhóm trong tháng 12 năm 2026."
- Update: "Dự án triển khai ERP giai đoạn 1 đang chậm 2 tuần so với kế hoạch; cần bổ sung 2 kỹ sư trước ngày 20 tháng 11 năm 2026 để kịp nghiệm thu ngày 15 tháng 12."

The sentence is done when it names the decision or the status, the key number, and the date. When the user's material does not contain them, ask for exactly the missing item; a one-pager without its ask is a report, not a one-pager.

## 2. Fill the skeleton

**Proposal** (tờ trình, đề xuất). Open with the lead sentence, ending in "với các nội dung sau:", then:

1. **Lý do**: two or three facts with numbers that make the proposal necessary now.
2. **Phương án đề xuất**: what, how much, by when, who carries it out. One line for each alternative considered and why it lost.
3. **Hiệu quả và rủi ro**: the measurable result, and the one or two main risks with how each is handled.
4. **Đề nghị**: the attachment list, then the closing request: "Phòng Hành chính - Nhân sự kính trình Giám đốc xem xét, phê duyệt./."

**Update** (báo cáo nhanh, cập nhật tiến độ):

1. **Tình hình chung**: the lead sentence, with the one number that proves the status (đúng tiến độ, chậm, vượt).
2. **Kết quả so với kế hoạch**: three to five figures, each as "đạt 18/20 hạng mục (90%)".
3. **Vấn đề và hướng xử lý**: each problem with its owner and date.
4. **Việc tiếp theo**: two to four items for the next period, with dates.
5. **Đề xuất, kiến nghị**: what you need from the reader, or "Không có kiến nghị phát sinh."

## 3. Fit the page

A tờ trình or báo cáo in the Nghị định 30 layout (full header, Kính gửi, signature, Times New Roman 14 pt) fits one A4 page with a body of at most 275 chữ, whether it has 5, 8 or 11 paragraphs; 300 to 325 chữ fit only when the line breaks fall well (measured by rendering with LibreOffice 26.8 on 2026-11-02). Aim for **250 chữ**, which leaves room for a placeholder to grow into a real number. Count chữ as space-separated syllables, the way `wc -w` counts them, over the căn cứ lines and the body together.

The page keeps the ask, every total, every deadline and every owner. When over budget, move detail into a phụ lục in this order until it fits:

1. Background history and method.
2. Full tables and breakdowns. The page keeps the total and points to the breakdown: "Tổng kinh phí 85.000.000 đồng (chi tiết tại Phụ lục I)."
3. The reasoning behind rejected alternatives. Each keeps one line.
4. Lists of names, units and items.

Every paragraph holds at most three sentences. A table on the page earns its place only when it replaces longer prose and has at most four rows.

## 4. Plan the phụ lục

The page stands alone: a decider who never opens a phụ lục can still act. A phụ lục adds detail and evidence, never a new ask or a number that differs from the page.

- Number them in the order the page first cites them: one phụ lục is "Phụ lục", two or more are "Phụ lục I", "Phụ lục II".
- Cite each in the body where its detail would have gone: "(chi tiết tại Phụ lục II)".
- List them all in the paragraph before the closing request: "Hồ sơ kèm theo gồm: Phụ lục I. Dự toán kinh phí chi tiết; Phụ lục II. Báo giá của ba đơn vị đào tạo."
- A phụ lục whose content the user will bring later is still listed with its final title, so the page is complete now.

When the user later brings the detail for a phụ lục, add it under its listed number and title. If the detail changes a total on the page, correct the page in the same edit.

## 5. Deliver

- **Official** (a tờ trình or báo cáo to a superior, in the Nghị định 30 layout): call the Skill tool with "vi-official-doc" for its tone rules and its `.docx` builder. Use type `to-trinh` or `bao-cao`, and put each phụ lục in the spec's `appendices` list, in page order, with tables as `{"table": [...]}` blocks. Build with `--one-page`: the builder prints the page's chữ count, or refuses the spec when the page is over 275 chữ, and then you cut per step 3 and build again. Adding a phụ lục later means appending to `appendices` and rebuilding with the same flag.
- **Internal** (email, chat, slide, wiki): no Quốc hiệu header. The subject line carries the lead sentence: "[Cập nhật] ERP giai đoạn 1: chậm 2 tuần, cần bổ sung 2 kỹ sư trước 20/11". Call the Skill tool with "vi-writing" for the register and the translationese check. The same skeleton and budget apply.

## Done when

The lead sentence opens the page and names the decision or status, its number and its date; the căn cứ and body total at most 275 chữ and you report the count (from `--one-page` when a file was built); every number on the page came from the user or is a visible placeholder; every phụ lục cited on the page appears in the attachment list with the same number and title, and in `appendices` when a file was built.
