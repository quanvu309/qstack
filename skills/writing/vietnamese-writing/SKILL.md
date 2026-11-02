---
name: vietnamese-writing
description: Write, translate, or edit Vietnamese text so it reads native, not translated. Use whenever you produce Vietnamese (tiếng Việt), even one UI string or a short translation, and when reviewing Vietnamese text for văn dịch, xưng hô, or formatting.
---

# Vietnamese writing

The failure this skill fixes is **translationese** (văn dịch): grammatically correct Vietnamese that a native reader recognises as English in disguise. Models draft in English shapes and swap the words. Write the Vietnamese sentence a native writer would produce for the same meaning, then check it against the catalog below.

## 1. Fix the address pair

Every Vietnamese text speaks from one pronoun to another. Pick the **address pair** (cặp xưng hô) before the first sentence and hold it to the end. A `## Vietnamese voice` section in the project's `AGENTS.md` overrides this table; without one, pick by surface and say which pair you chose.

| Surface | Pair | Example |
| --- | --- | --- |
| Product UI, docs, onboarding | no pronoun, or chúng tôi / bạn | "Nhập email để tiếp tục." |
| Friendly consumer brand, community | mình / bạn | "Mình gửi bạn mã giảm giá nhé." |
| Bank, airline, hotel, insurer | chúng tôi / quý khách | "Quý khách vui lòng kiểm tra lại số tài khoản." |
| Shop chat, sales, support agent | em / anh or chị (anh/chị when unknown) | "Dạ, em kiểm tra đơn cho anh/chị ngay ạ." |
| Personal blog, essay | tôi / bạn (or các bạn) | "Tôi đã thử cách này suốt ba tháng." |

Drop the pronoun whenever the sentence stands without it. Vietnamese omits subjects that English must state, so "Bạn có thể... Bạn cũng có thể... Bạn sẽ..." is translationese even when every pronoun is correct.

## 2. Pick the register

Hán Việt words raise the register. Formal documents, contracts and legal text keep them. UI copy, chat and blog posts take the thuần Việt word when one exists:

- sử dụng → dùng; tiến hành cài đặt → cài đặt; thực hiện + noun → the verb itself (thực hiện thanh toán → thanh toán)
- nhằm mục đích → để; đối với → với; hiện tại as an adverb → hiện ("Hiện chưa có đơn hàng"), but keep it as the adjective "current" ("Mật khẩu hiện tại")
- Keep a loanword the audience says aloud (email, app, link). Translate one they would not (feature → tính năng).

## 3. Write, then run the translationese catalog

Check every sentence against every pattern. A pattern that fires gets rewritten as a whole sentence, never patched word by word.

1. **Passive with "được/bị... bởi".** "Báo cáo đã được hoàn thành bởi nhóm." → "Nhóm đã làm xong báo cáo." Name the actor as subject. "Bởi" introducing an agent is the strongest single tell.
2. **"Một cách" + adjective.** "xử lý một cách nhanh chóng" → "xử lý nhanh".
3. **Nominalising with "việc", "sự".** "Việc sử dụng ứng dụng này mang lại sự tiết kiệm đáng kể về thời gian." → "Ứng dụng này giúp bạn tiết kiệm khá nhiều thời gian." Use the verb.
4. **"Của bạn" for every "your".** "Vui lòng nhập mật khẩu của bạn." → "Nhập mật khẩu." Possession is implied.
5. **"Các/những" for every English plural.** "Các người dùng có thể xuất các báo cáo." → "Người dùng có thể xuất báo cáo."
6. **"Có thể" on an instruction.** "Bạn có thể nhấn vào đây để tải về." → "Nhấn vào đây để tải về." Keep "có thể" when permission or possibility is the point: "Bạn có thể hủy vé bất cứ lúc nào."
7. **"Điều này" opening sentence after sentence.** One is native; a run of them is English "This...". "Điều này có nghĩa là bạn cần cập nhật." → join it to the previous clause ("..., nên bạn cần cập nhật.") or open with "Tức là".
8. **Calqued idioms.** "chơi một vai trò" (play a role), "vào cuối ngày" (at the end of the day), "cảm thấy tự do liên hệ" (feel free), "ở trên cùng một trang" (on the same page). Use the Vietnamese idiom ("có vai trò", "suy cho cùng", "đừng ngại liên hệ", "thống nhất với nhau") or say it plainly.
9. **Stock phrases and stacked connectives.** Cut "đóng vai trò quan trọng", "trong bối cảnh...", "hãy cùng khám phá", "hành trình", "nâng tầm", "kỷ nguyên số", "giải pháp toàn diện", "trải nghiệm tuyệt vời", and write the specific claim instead. The connectives "ngoài ra", "hơn nữa", "không chỉ... mà còn" and "tóm lại" are native; the tell is one per paragraph. Use each at most once per text, never to open consecutive paragraphs, and no "tóm lại" on a text too short to need a summary.
10. **"Hãy" on every instruction.** UI labels and steps take the bare verb ("Lưu", "Chọn tệp"). "Hãy" reads as preaching; keep it for an occasional call to action in marketing.
11. **English punctuation habits.** Title Case headings ("Hướng Dẫn Sử Dụng" → "Hướng dẫn sử dụng"), the long dash (U+2014) as a clause joiner, chains of colons and semicolons. Use commas and full stops.
12. **Long noun-stack subjects.** "Quy trình kiểm tra chất lượng sản phẩm đầu ra của nhà máy đã được cải thiện." → "Nhà máy đã cải thiện khâu kiểm tra chất lượng đầu ra."

## 4. UI copy

- Buttons are a verb, one to three syllables when possible: "Lưu", "Hủy", "Tiếp tục", "Đăng nhập".
- Errors say what happened, then what to do: "Mật khẩu chưa đúng. Thử lại hoặc đặt lại mật khẩu."
- Use "chưa" for a state the user can change ("Chưa có đơn hàng nào", "Email chưa được xác minh"); keep "không" for what will not change ("Không tìm thấy trang").
- "Vui lòng" once per message at most, and only where politeness carries weight (a request, an apology).

## 5. Format

Headings are sentence case. Numbers, money, dates, times, quotes, tone mark placement and capitalisation of names and organisations follow [CONVENTIONS.md](CONVENTIONS.md). Read it whenever the text contains any of those.

## Done when

Every sentence has passed every catalog pattern, the address pair is the same from first line to last, and a native reader would not guess the text started in English. When editing someone else's text, report each rewrite as `before → after` with the pattern number, so the writer learns the pattern.
