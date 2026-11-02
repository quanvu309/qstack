# qstack

Skill giúp AI agent (Claude Code, Codex, Cursor...) viết tiếng Việt tự nhiên, soạn văn bản đúng thể thức và dựng giao diện hợp với người Việt.

Agent viết tiếng Việt đúng ngữ pháp mà đọc vẫn ra giọng dịch: "được thực hiện bởi", "một cách nhanh chóng", câu nào cũng "của bạn". Dựng giao diện thì chọn font thiếu chữ "ơ, ư", để chữ hoa mất dấu, xếp "Đông" sau "Zô", và vẫn hỏi "quận/huyện" dù cấp huyện đã bỏ từ 1/7/2025. Mỗi skill ở đây sửa một nhóm lỗi như vậy.

Skill nào cũng ngắn, dễ sửa và ghép được với nhau. Cứ fork rồi chỉnh cho hợp dự án.

> **English.** Agent skills for Vietnamese: native prose without translationese, official documents and one-pagers built as .docx in the Nghị định 30/2020 layout, typography that keeps diacritics whole, and forms, search and formatting that fit Vietnamese names, addresses, phone numbers, money and dates.

## Ví dụ

`vi-one-pager` soạn tờ trình một trang: đề nghị nằm ngay câu đầu, dự toán chi tiết dời sang Phụ lục II. Phụ lục nào cũng bắt đầu ở trang mới và có số trang riêng.

![Tờ trình một trang bên cạnh phụ lục dự toán chi phí](https://github.com/quanvu309/qstack/releases/latest/download/one-pager.png)

`vi-official-doc` dựng quyết định bổ nhiệm và công văn thành file .docx theo thể thức Nghị định 30/2020/NĐ-CP: Quốc hiệu, Tiêu ngữ, số và ký hiệu, trích yếu, nơi nhận, chữ ký.

![Quyết định bổ nhiệm bên cạnh công văn, theo thể thức Nghị định 30](https://github.com/quanvu309/qstack/releases/latest/download/official-documents.png)

## Cài đặt

Mỗi agent chỉ cài một cách. Cài cả plugin lẫn skills.sh thì skill nào cũng hiện hai lần.

<details>
<summary><strong>Claude Code</strong> (tự cập nhật)</summary>

```bash
claude plugin marketplace add quanvu309/qstack
claude plugin install qstack@qstack
```

</details>

<details>
<summary><strong>Codex</strong> (tự cập nhật)</summary>

```bash
codex plugin marketplace add quanvu309/qstack
codex plugin add qstack@qstack
```

</details>

<details>
<summary><strong>Agent khác, hoặc muốn sửa file</strong> (cập nhật tay)</summary>

```bash
npx skills@latest add quanvu309/qstack
```

Cập nhật bằng `npx skills@latest update`. Chạy lại `add` để lấy skill mới.

</details>

Cài xong, chạy `/vi-setup` một lần trong mỗi dự án để chốt giọng văn: xưng hô, kiểu đặt dấu (hòa hay hoà), cách ghi tiền (đ, ₫ hay VND). Kết quả ghi vào `AGENTS.md`, skill nào cũng đọc theo.

## Viết

### Gọi tay

- **[vi-setup](./skills/writing/vi-setup/SKILL.md)**: Chốt giọng văn tiếng Việt của dự án một lần (xưng hô, văn phong, kiểu đặt dấu, cách ghi tiền và ngày) để mọi skill viết giống nhau.

### Agent tự gọi

- **[vi-writing](./skills/writing/vi-writing/SKILL.md)**: Viết, dịch và sửa tiếng Việt cho ra giọng người Việt: giữ một cặp xưng hô từ đầu đến cuối, chọn văn phong, rà 12 kiểu văn dịch, ghi đúng số, tiền, ngày tháng.

## Văn bản

### Agent tự gọi

- **[vi-official-doc](./skills/documents/vi-official-doc/SKILL.md)**: Soạn văn bản hành chính (quyết định, công văn, tờ trình, thông báo, báo cáo, kế hoạch, biên bản, giấy mời, giấy giới thiệu) đúng văn phong và thể thức Nghị định 30/2020/NĐ-CP, xuất ra file .docx.
- **[vi-one-pager](./skills/documents/vi-one-pager/SKILL.md)**: Viết tờ trình, báo cáo nhanh hay đề xuất gọn trong một trang: đề nghị hoặc tình hình nằm ngay câu đầu, chi tiết dời sang phụ lục, bổ sung sau cũng được.

## Thiết kế

### Agent tự gọi

- **[vi-typography](./skills/design/vi-typography/SKILL.md)**: Chọn font đủ chữ tiếng Việt, giữ dấu không bị cắt, không để dòng ngắt giữa số và đơn vị. Kèm script báo font thiếu chữ nào.
- **[vi-locale](./skills/design/vi-locale/SKILL.md)**: Làm form, tìm kiếm, sắp xếp và định dạng hợp với người dùng Việt Nam: họ tên, địa chỉ hai cấp, số điện thoại, tiền đồng, ngày tháng, chữ có dấu.

## Đóng góp

Cách báo lỗi và gửi pull request nằm trong [CONTRIBUTING.md](./CONTRIBUTING.md). Giấy phép [MIT](./LICENSE).
