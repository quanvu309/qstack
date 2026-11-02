# qstack

**Để AI agent viết tiếng Việt như người Việt, soạn văn bản đúng thể thức và dựng giao diện không mất dấu.**

Agent viết tiếng Việt đúng ngữ pháp mà đọc vẫn ra giọng dịch, dựng form vẫn hỏi "quận/huyện", xếp tên thì để "Đông" sau "Zô". qstack gồm sáu skill cho Claude Code, Codex, Cursor và agent khác, mỗi skill sửa một nhóm lỗi như vậy. Bảng dưới đặt câu agent hay viết cạnh câu người Việt viết cho cùng ý.

| | Agent hay viết | Người Việt viết |
| --- | --- | --- |
| Câu bị động | Báo cáo đã được hoàn thành bởi nhóm. | Nhóm đã làm xong báo cáo. |
| Danh từ hóa | Việc sử dụng ứng dụng này mang lại sự tiết kiệm đáng kể về thời gian. | Ứng dụng này giúp bạn tiết kiệm khá nhiều thời gian. |
| "Của bạn", "có thể" | Bạn có thể nhấn vào đây để tải về các tệp của bạn. | Nhấn vào đây để tải tệp về. |
| Báo lỗi | Mật khẩu của bạn không chính xác. | Mật khẩu chưa đúng. Thử lại hoặc đặt lại mật khẩu. |
| Trạng thái trống | Không có đơn hàng nào. | Chưa có đơn hàng nào. |
| Xưng hô khi chat bán hàng | Bạn vui lòng chờ, chúng tôi sẽ kiểm tra đơn hàng của bạn. | Dạ, em kiểm tra đơn cho anh/chị ngay ạ. |
| Tiêu đề, tiền, ngày | Hướng Dẫn Thanh Toán: 250.000,00 VND trước 11/2/2026 | Hướng dẫn thanh toán: 250.000 đ trước 2/11/2026 |

> **English.** Agent skills for Vietnamese: native prose without translationese, official documents and one-pagers built as .docx in the Nghị định 30/2020 layout, typography that keeps diacritics whole, and forms, search, sorting and formatting that fit Vietnamese names, addresses, phone numbers, money and dates.

## Văn bản ra file .docx

![Tờ trình một trang, đề nghị nằm ở câu đầu, bên cạnh phụ lục dự toán chi phí](https://github.com/quanvu309/qstack/releases/latest/download/one-pager.png)

`vi-one-pager`: tờ trình gọn trong một trang A4. Đề nghị và số tiền nằm ngay câu đầu. Dự toán chi tiết dời sang Phụ lục II, phụ lục nào cũng sang trang mới và đánh số trang riêng từ 1. Khi dựng file với `--one-page`, script đếm chữ của trang chính và không dựng nếu quá 275 chữ, mức vừa một trang A4 theo thể thức Nghị định 30.

![Quyết định bổ nhiệm bên cạnh công văn, theo thể thức Nghị định 30/2020/NĐ-CP](https://github.com/quanvu309/qstack/releases/latest/download/official-documents.png)

`vi-official-doc`: quyết định bổ nhiệm và công văn theo thể thức Nghị định 30/2020/NĐ-CP, với Quốc hiệu, Tiêu ngữ, số và ký hiệu, trích yếu, nơi nhận, chữ ký. Số liệu người dùng chưa đưa thì để trống trong ngoặc vuông, như "[số tài khoản]", thay vì bịa ra.

## Giao diện và dữ liệu

Những lỗi chỉ lộ ra khi có dữ liệu tiếng Việt thật:

- **Sắp xếp.** Hàm sort mặc định xếp theo mã ký tự, nên "Ăn" và "Đông" đứng sau "Zô".

  ```js
  ["Zô", "Đông", "Ăn", "An"].sort();                                // ["An", "Zô", "Ăn", "Đông"]
  ["Zô", "Đông", "Ăn", "An"].sort(new Intl.Collator("vi").compare); // ["An", "Ăn", "Đông", "Zô"]
  ```

- **Bỏ dấu để tìm kiếm.** "đ" là một chữ riêng, không phải "d" cộng dấu, nên bỏ dấu xong vẫn còn "đ". Gõ "duong" sẽ không tìm ra "Đường" nếu không đổi riêng chữ này.

  ```js
  "Đường Hà Nội".normalize("NFD").replace(/\p{M}/gu, ""); // "Đuong Ha Noi"
  ```

- **Tiền.** `parseFloat("1.000.000")` trả về `1`. `Intl` định dạng VND thì tự làm tròn số lẻ và chèn khoảng trắng không ngắt (U+00A0) trước ₫, test so chuỗi sẽ hỏng nếu không tính đến.
- **Địa chỉ.** Từ 1/7/2025 không còn cấp huyện: form chỉ cần tỉnh/thành phố (34 đơn vị), xã/phường, rồi số nhà và đường (Nghị quyết 202/2025/QH15 và Luật Tổ chức chính quyền địa phương số 72/2025/QH15, kiểm tra ngày 2/11/2026). Danh sách 63 tỉnh hay ô "quận/huyện" là đã cũ.
- **Font.** Font có "á" vẫn có thể thiếu "ơ, ư, ạ, ẫ". Khi đó trình duyệt lấy font khác vẽ riêng mấy chữ đó, chữ trông như ghép từ hai kiểu font. Script sau liệt kê mọi chữ, dấu và ký hiệu ₫ font còn thiếu, rồi trả mã lỗi 1 để chặn được trong CI. Chạy từ thư mục `skills/design/vi-typography`:

  ```bash
  uv run --with fonttools scripts/check-font.py <font-files>
  ```

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
