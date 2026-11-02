# qstack

Bộ skill cho AI agent (Claude Code, Codex, Cursor...) để viết và thiết kế cho người Việt.

Agent viết tiếng Việt đúng ngữ pháp nhưng đọc lên vẫn ra giọng dịch từ tiếng Anh: "được thực hiện bởi", "một cách nhanh chóng", "của bạn" ở mọi câu. Khi dựng giao diện, agent chọn font thiếu chữ "ơ, ư", để dòng chữ hoa bị cắt mất dấu, xếp "Đông" sau "Zô", và vẫn hỏi "quận/huyện" dù cấp huyện đã bỏ từ ngày 1/7/2025. Các skill ở đây sửa từng lỗi đó.

Mỗi skill đều ngắn, dễ sửa và ghép được với nhau. Bạn cứ fork và chỉnh theo dự án của mình.

> **English.** Agent skills for writing and designing in Vietnamese: native prose without translationese, typography that keeps diacritics whole, and forms that fit Vietnamese names, addresses and money.

## Ví dụ

Tờ trình một trang do `vietnamese-one-pager` soạn: đề nghị nằm ngay đoạn đầu, dự toán chi tiết chuyển sang Phụ lục II. Mỗi phụ lục sang trang mới và đánh số trang riêng.

![Tờ trình một trang và phụ lục dự toán chi phí](https://github.com/quanvu309/qstack/releases/latest/download/one-pager.png)

Quyết định bổ nhiệm và công văn do `vietnamese-official-document` dựng thành file .docx, đúng thể thức Nghị định 30/2020/NĐ-CP: Quốc hiệu, Tiêu ngữ, số và ký hiệu, trích yếu, nơi nhận, chữ ký.

![Quyết định bổ nhiệm và công văn theo thể thức Nghị định 30](https://github.com/quanvu309/qstack/releases/latest/download/official-documents.png)

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
- **[vietnamese-official-document](./skills/writing/vietnamese-official-document/SKILL.md)**: Soạn văn bản hành chính (quyết định, công văn, tờ trình, thông báo, báo cáo, kế hoạch, biên bản, giấy mời, giấy giới thiệu) đúng văn phong hành chính và đúng thể thức Nghị định 30/2020/NĐ-CP, xuất ra file .docx.
- **[vietnamese-one-pager](./skills/writing/vietnamese-one-pager/SKILL.md)**: Viết tờ trình, báo cáo nhanh hay đề xuất gói gọn trong một trang, nêu đề nghị ngay câu đầu, chuyển chi tiết sang phụ lục để bổ sung sau.

## Thiết kế

### Agent tự gọi

- **[vietnamese-typography](./skills/design/vietnamese-typography/SKILL.md)**: Chọn font đủ chữ tiếng Việt, giữ dấu không bị cắt, ngắt dòng đúng. Có script kiểm tra font thiếu ký tự nào.
- **[vietnamese-locale](./skills/design/vietnamese-locale/SKILL.md)**: Làm form, tìm kiếm, sắp xếp và định dạng cho dữ liệu của người dùng Việt Nam: họ tên, địa chỉ hai cấp, số điện thoại, tiền đồng, ngày tháng, chữ có dấu.

## Đóng góp

Đọc [CONTRIBUTING.md](./CONTRIBUTING.md). Giấy phép [MIT](./LICENSE).
