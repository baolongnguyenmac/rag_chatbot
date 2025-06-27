[![CI and CD to HuggingSpace](https://github.com/baolongnguyenmac/rag_chatbot/actions/workflows/main.yml/badge.svg)](https://github.com/baolongnguyenmac/rag_chatbot/actions/workflows/main.yml)

# Video RAG Chatbot

## Flow

![](./img/flow.svg)

1. Data processing

    - Download video và subtitle từ YouTube
    - Chunking subtitle theo từng đoạn thoại --> Nhúng các chunks vào DB
    - Chunking video theo từng khung hình ở giữa đoạn thoại --> Nhúng các frame vào DB kèm theo metadata của từng frame (`timestamp`, `subtitle`, `frame_path`)

2. Query from ReAct agent

    - Tạo một ReAct agent: Cho phép quyết định tool nào được gọi, gọi bao nhiêu lần, dựa vào query
    - Tools: Tất cả các tools sau đều trả về text
        - `text_search`: Áp dụng cho những câu hỏi có thể trả lời bằng `TextVectorDB`. Ví dụ: Brand Apple được nhắc đến lần đầu trong video vào thời điểm nào?
        - `img_search_by_img`: Truy vấn ảnh với một query image
        - `img_search_by_text`: Truy vấn ảnh bằng một mô tả. Ví dụ: Liệt kê các khoảnh khắc có xuất hiện hình ảnh iPhone

## Demo

- Giới thiệu về flow (bên trên)

- Chạy code
    - Xóa database, để lại video + sub
    - Bật và giới thiệu video
    - Khởi chạy chatbot: `python -m chat_rag`: Giới thiệu về quá trình khởi tạo mọi thứ

    - Bật file phụ đề và frame cùng với prompt
    - Prompt:
        - Hỏi đáp qua hình ảnh: `list out all moments (timestamp, subtitle, path to frame) that are related to this image`

        - Hỏi đáp qua phụ đề:
            - `according to the video, what could be addressed if there was something special that you could do on a tablet?`
            - `sample 3 moments that are related to the term "Android tablet"`

        - Hỏi đáp qua mô tả hình ảnh: `according to the video, list out all moments that are related to or contains the image of an iPhone`

- Trình bày về TODO

## TODO

- Viết tool tự động crawl video và subtitle rồi bỏ vào db
- Dùng multimodal embedding --> chỉ yêu cầu 1 embedding
- Tách riêng quá trình chunking khỏi quá trình thêm dữ liệu vào db
- Deploy

## Problems

- Khi chuyển sang video hoạt hình thì truy vấn embedding không còn tốt nữa