# Đóng góp

Rất mong bạn góp ý. Skill chỉ đổi khi có lỗi thật, nên issue có ích nhất là kể lại một lần bạn thấy agent làm sai.

## Báo lỗi một skill

Mở issue, ghi rõ:

1. Bạn đã chạy gì: tên skill, câu lệnh, agent (Claude Code, Codex...).
2. Agent viết hoặc làm gì. Dán nguyên văn đoạn sai.
3. Người Việt sẽ viết hoặc làm thế nào. Nếu là quy tắc chính tả, luật hay số liệu, ghi kèm nguồn.

Mỗi issue một lỗi. Nhiều lỗi thì mở nhiều issue.

## Gửi pull request

- Chạy `node scripts/check.mjs` trước khi gửi. CI chạy lại lệnh này.
- Viết skill theo quy ước trong [AGENTS.md](./AGENTS.md): phần thân skill bằng tiếng Anh, mọi ví dụ bằng tiếng Việt tự nhiên.
- Thông tin có thể thay đổi (đơn vị hành chính, đầu số điện thoại, văn bản luật) phải ghi nguồn và ngày kiểm tra.

## Đề xuất skill mới

Mở Discussion và kể lại tình huống agent làm sai mà skill hiện có chưa xử lý. Nếu ghép các skill hiện có lại là đủ thì không cần skill mới.
