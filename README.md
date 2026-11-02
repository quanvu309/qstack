# qstack

Bộ skill giúp AI agent làm việc bằng tiếng Việt như người Việt.

Agent học viết chủ yếu qua văn bản tiếng Anh, nên khi làm việc bằng tiếng Việt nó vẫn giữ thói quen của tiếng Anh: cách đặt câu, cách trình bày văn bản, cách ghi số liệu. Người Việt đọc là nhận ra. qstack ghi những quy ước người Việt vẫn ngầm hiểu thành skill để agent làm theo.

> **English:** agent skills that teach AI agents the conventions of working in Vietnamese.

## qstack làm việc ra sao

- Mỗi skill lo một việc và dựa vào nhau: skill soạn văn bản gọi skill viết để câu chữ cùng một giọng.
- Phần lớn skill tự chạy khi agent gặp đúng việc. Skill nào cần bạn quyết thì bạn gọi tay.
- Giọng văn của dự án chốt một lần bằng `/vi-setup`, mọi skill viết theo.
- Quy ước nào đổi theo luật hay theo thời gian thì skill ghi nguồn và ngày kiểm tra.

## Ví dụ

![Tờ trình một trang và phụ lục](https://github.com/quanvu309/qstack/releases/latest/download/one-pager.png)

![Quyết định và công văn theo thể thức nhà nước](https://github.com/quanvu309/qstack/releases/latest/download/official-documents.png)

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

Cài xong, chạy `/vi-setup` một lần trong mỗi dự án.

## Viết

Giọng văn và câu chữ.

### Gọi tay

- **[vi-setup](./skills/writing/vi-setup/SKILL.md)**: Chốt giọng văn tiếng Việt của dự án để mọi skill viết cùng một giọng.

### Agent tự gọi

- **[vi-writing](./skills/writing/vi-writing/SKILL.md)**: Viết, dịch và sửa tiếng Việt cho ra giọng người Việt.

## Văn bản

Văn bản theo thể thức của cơ quan, doanh nghiệp Việt Nam.

### Agent tự gọi

- **[vi-official-doc](./skills/documents/vi-official-doc/SKILL.md)**: Soạn văn bản hành chính đúng văn phong và thể thức, xuất ra file .docx.
- **[vi-one-pager](./skills/documents/vi-one-pager/SKILL.md)**: Viết tờ trình, báo cáo, đề xuất gọn trong một trang, chi tiết để ở phụ lục.

## Thiết kế

Giao diện và dữ liệu cho người dùng Việt.

### Agent tự gọi

- **[vi-typography](./skills/design/vi-typography/SKILL.md)**: Chọn font và trình bày chữ để dấu tiếng Việt không mất, không chồng nhau.
- **[vi-locale](./skills/design/vi-locale/SKILL.md)**: Lưu, tìm và hiển thị tên, địa chỉ, tiền, ngày tháng theo cách người Việt quen dùng.

## Đóng góp

Muốn báo lỗi hay đề xuất skill mới, xem [CONTRIBUTING.md](./CONTRIBUTING.md). Giấy phép [MIT](./LICENSE).
