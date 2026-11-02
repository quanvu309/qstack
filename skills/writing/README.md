# Viết

Skill cho văn bản tiếng Việt: bài viết, email, tài liệu, chữ trên giao diện.

## Gọi tay

Chỉ chạy khi bạn gõ tên skill (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` trong `agents/openai.yaml`).

- **[setup-qstack](./setup-qstack/SKILL.md)**: Chốt giọng văn tiếng Việt của dự án một lần (xưng hô, văn phong, kiểu đặt dấu) để mọi skill viết giống nhau.

## Agent tự gọi

Agent tự chọn khi việc đang làm khớp với mô tả. Bạn cũng có thể gõ tên skill để gọi trực tiếp.

- **[vietnamese-writing](./vietnamese-writing/SKILL.md)**: Viết, dịch và sửa văn bản tiếng Việt cho tự nhiên như người Việt viết, không mang giọng dịch.
- **[vietnamese-official-document](./vietnamese-official-document/SKILL.md)**: Soạn văn bản hành chính đúng văn phong và thể thức Nghị định 30/2020/NĐ-CP, xuất ra file .docx.
