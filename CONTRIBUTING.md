# Đóng góp

Góp ý nào cũng quý. Skill chỉ đổi khi có lỗi thật, nên issue có ích nhất là kể lại một lần agent làm sai.

## Báo lỗi một skill

Mở issue, ghi rõ:

1. Đã chạy gì: tên skill, câu lệnh, agent (Claude Code, Codex...).
2. Agent viết hoặc làm gì. Dán nguyên văn đoạn sai.
3. Người Việt sẽ viết hoặc làm thế nào. Nếu là quy tắc chính tả, luật hay số liệu, ghi kèm nguồn.

Mỗi issue một lỗi. Nhiều lỗi thì mở nhiều issue.

## Gửi pull request

- Chạy `node scripts/check.mjs` trước khi gửi. CI chạy lại lệnh này.
- Viết skill theo quy ước trong [AGENTS.md](./AGENTS.md): thân skill bằng tiếng Anh, ví dụ nào cũng bằng tiếng Việt tự nhiên.
- Thông tin có thể đổi (đơn vị hành chính, đầu số điện thoại, văn bản luật) phải ghi nguồn và ngày kiểm tra.

## Đề xuất skill mới

Mở Discussion, kể lại tình huống agent làm sai mà chưa skill nào xử lý. Ghép các skill sẵn có mà đủ thì không cần skill mới.
