# qstack

Bộ skill giúp agent viết tiếng Việt không còn giọng dịch.

Hỏi agent bằng tiếng Việt, câu trả lời thường đúng chính tả nhưng người Việt đọc là biết dịch từ tiếng Anh: "được thực hiện bởi", "một cách nhanh chóng", "của bạn" ở gần như mọi câu. Dùng được với Claude Code, Codex, Cursor và các agent đọc được skill.

> **English:** agent skills for writing, official documents and UI in Vietnamese.

## Trước và sau

| Tình huống | Agent thường viết | Có qstack |
| --- | --- | --- |
| Báo lỗi đăng nhập | Mật khẩu của bạn không chính xác. Vui lòng thử lại. | Mật khẩu chưa đúng. Thử lại hoặc đặt lại mật khẩu. |
| Một câu trong báo cáo | Việc triển khai hệ thống đã được hoàn thành bởi phòng IT. | Phòng IT đã triển khai xong hệ thống. |
| Nhắn khách hàng | Bạn vui lòng chờ, chúng tôi sẽ kiểm tra đơn hàng của bạn. | Dạ, anh/chị chờ em chút, em kiểm tra đơn ngay ạ. |
| Giỏ hàng trống | Không có sản phẩm nào trong giỏ hàng của bạn. | Giỏ hàng chưa có sản phẩm nào. |
| Tiêu đề, tiền, ngày | Hướng Dẫn Thanh Toán: 250,000 VND trước 11/2/2026 | Hướng dẫn thanh toán: 250.000 đ trước 2/11/2026 |

## Công văn, tờ trình ra file .docx

![Tờ trình một trang, đề nghị nằm ở câu đầu, bên cạnh phụ lục dự toán chi phí](https://github.com/quanvu309/qstack/releases/latest/download/one-pager.png)

Tờ trình một trang do `vi-one-pager` soạn. Ngay câu đầu đã nêu đề nghị và số tiền. Bảng dự toán nằm ở Phụ lục II, sang trang mới và đánh số trang riêng. Trang chính dài quá 275 chữ thì script không xuất file và nhắc dời bớt chi tiết sang phụ lục.

![Quyết định bổ nhiệm bên cạnh công văn, theo thể thức Nghị định 30/2020/NĐ-CP](https://github.com/quanvu309/qstack/releases/latest/download/official-documents.png)

Quyết định và công văn do `vi-official-doc` trình bày theo thể thức Nghị định 30/2020/NĐ-CP, từ Quốc hiệu, số ký hiệu đến nơi nhận và chữ ký. Thiếu thông tin nào, như số tài khoản, skill ghi "[số tài khoản]" để bạn điền, chứ không tự bịa.

## Lỗi chỉ gặp với dữ liệu tiếng Việt

- **Sắp xếp.** Hàm sort mặc định xếp theo mã ký tự, nên "Ăn" và "Đông" đứng sau "Zô".

  ```js
  ["Zô", "Đông", "Ăn", "An"].sort();                                // ["An", "Zô", "Ăn", "Đông"]
  ["Zô", "Đông", "Ăn", "An"].sort(new Intl.Collator("vi").compare); // ["An", "Ăn", "Đông", "Zô"]
  ```

- **Tìm kiếm không dấu.** "đ" là một chữ riêng chứ không phải "d" thêm dấu, nên bỏ dấu xong vẫn còn "đ" và gõ "duong" không ra "Đường".

  ```js
  "Đường Hà Nội".normalize("NFD").replace(/\p{M}/gu, ""); // "Đuong Ha Noi"
  ```

- **Tiền.** `parseFloat("1.000.000")` trả về `1`. `Intl` in tiền đồng có khoảng trắng không ngắt (U+00A0) trước ₫, nên test so chuỗi hay hỏng đúng chỗ này.
- **Địa chỉ.** Từ 1/7/2025 không còn cấp huyện. Form chỉ cần tỉnh/thành phố (34 đơn vị), xã/phường, rồi số nhà và tên đường (Nghị quyết 202/2025/QH15 và Luật Tổ chức chính quyền địa phương số 72/2025/QH15, kiểm tra ngày 2/11/2026).
- **Font.** Font có "á" vẫn có thể thiếu "ơ, ư, ạ, ẫ", và trình duyệt mượn font khác cho riêng mấy chữ đó. Chạy lệnh dưới đây trong `skills/design/vi-typography` để in ra những chữ còn thiếu; lệnh thoát với mã 1 nên CI báo lỗi.

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

- **[vi-writing](./skills/writing/vi-writing/SKILL.md)**: Viết, dịch và sửa tiếng Việt cho ra giọng người Việt: giữ một cặp xưng hô từ đầu đến cuối, chọn văn phong, rà 16 kiểu câu nghe như dịch hay như máy viết, ghi đúng số, tiền, ngày tháng.

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
