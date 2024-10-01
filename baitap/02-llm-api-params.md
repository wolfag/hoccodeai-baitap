# Đề bài

Toàn bộ các bài tập đều là ứng dụng console

1. Viết một ứng dụng console đơn giản, người dùng gõ câu hỏi vào console, bot trả lời và in ra. Có thể dùng `stream` hoặc `non-stream`.
2. Cải tiến ứng dụng chat: Sau mỗi câu hỏi và trả lời, ta lưu vào array `messages` và tiếp tục gửi lên API để bot nhớ nội dung trò chuyện.

3. Tóm tắt website. Dán link website vào console, bot sẽ tóm tắt lại nội dung của website đó.

   1. Người dùng dán link <https://tuoitre.vn/cac-nha-khoa-hoc-nga-bao-tu-manh-nhat-20-nam-sap-do-bo-trai-dat-2024051020334196.htm> vào console
   2. Sử dụng `requests` để lấy nội dung website.
   3. Dùng thư viện `beautifulsoup4` để parse HTML. (Bạn có thể hardcode lấy thông tin từ div có id là `main-detail` ở vnexpress)
   4. Bạn cũng có thể thay bước 2-3 bằng cách dùng <https://jina.ai/reader/>, thên `r.jina.ai` để lấy nội dung website.
   5. Viết prompt và gửi nội dung đã parse lên API để tóm tắt. (Xem lại bài prompt engineering nha!)

4. Dịch nguyên 1 file dài từ ngôn ngữ này sang ngôn ngữ khác.

   1. Viết prompt để set giọng văn, v...v
   2. Đọc từ file gốc, sau đó cắt ra thành từng phần để dịch vì LLM có context size có hạn
   3. Sau khi dịch xong, gom kết quả lại, ghi vào file mới.

5. Dùng bot để... giải bài tập lập trình. Viết ứng dụng console cho phép bạn đưa câu hỏi vào, bot sẽ viết code Python/JavaScript. Sau đó, viết code lưu đáp án vào file `final.py` và chạy thử. (Dùng Python sẽ dễ hơn JavaScript nhé!)

# Nội dung nộp bài

Mỗi bài sẽ là 1 file Python (.py) hoặc NodeJS (.js/ts) hoặc ngôn ngữ gì tuỳ các bạn thích.