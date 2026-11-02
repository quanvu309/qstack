# qstack

Bộ skill cho AI agent (Claude Code, Codex, Cursor...) để viết và thiết kế cho người Việt.

Agent viết tiếng Việt đúng ngữ pháp nhưng đọc lên vẫn ra giọng dịch từ tiếng Anh: "được thực hiện bởi", "một cách nhanh chóng", "của bạn" ở mọi câu. Khi dựng giao diện, agent chọn font thiếu chữ "ơ, ư", để dòng chữ hoa bị cắt mất dấu, xếp "Đông" sau "Zô", và vẫn hỏi "quận/huyện" dù cấp huyện đã bỏ từ ngày 1/7/2025. Các skill ở đây sửa từng lỗi đó.

Mỗi skill đều ngắn, dễ sửa và ghép được với nhau. Bạn cứ fork và chỉnh theo dự án của mình.

> **English.** Agent skills for writing and designing in Vietnamese: native prose without translationese, typography that keeps diacritics whole, and forms that fit Vietnamese names, addresses and money.

## Cài đặt

Chọn một cách cho mỗi agent. Cài cả plugin lẫn skills.sh thì mỗi skill sẽ xuất hiện hai lần.

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

Sau khi cài, chạy `/setup-qstack` một lần trong mỗi dự án để chốt giọng văn: xưng hô, kiểu đặt dấu (hòa hay hoà), cách ghi tiền (đ, ₫ hay VND).

## Viết

### Gọi tay

- **[setup-qstack](./skills/writing/setup-qstack/SKILL.md)**: Chốt giọng văn tiếng Việt của dự án một lần (xưng hô, văn phong, kiểu đặt dấu) để mọi skill viết giống nhau.

### Agent tự gọi

- **[vietnamese-writing](./skills/writing/vietnamese-writing/SKILL.md)**: Viết, dịch và sửa văn bản tiếng Việt cho tự nhiên như người Việt viết: giữ một cặp xưng hô, chọn văn phong, rà 12 kiểu văn dịch, định dạng số, tiền, ngày tháng.

## Thiết kế

### Agent tự gọi

- **[vietnamese-typography](./skills/design/vietnamese-typography/SKILL.md)**: Chọn font đủ chữ tiếng Việt, giữ dấu không bị cắt, ngắt dòng đúng. Có script kiểm tra font thiếu ký tự nào.
- **[vietnamese-locale](./skills/design/vietnamese-locale/SKILL.md)**: Làm form, tìm kiếm, sắp xếp và định dạng cho dữ liệu của người dùng Việt Nam: họ tên, địa chỉ hai cấp, số điện thoại, tiền đồng, ngày tháng, chữ có dấu.

## Đóng góp

Đọc [CONTRIBUTING.md](./CONTRIBUTING.md). Giấy phép [MIT](./LICENSE).
