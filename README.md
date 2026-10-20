# Personal Link Hub & Developer Portfolio (Python)

Website cá nhân tĩnh, sinh bằng Python (Jinja2). Một file cấu hình duy nhất: `config.py`.
Kết quả là thư mục `dist/` chỉ gồm HTML/CSS/JS, đưa lên hosting nào cũng chạy và có một đường dẫn công khai.

## Cấu trúc

```
config.py            <- chỉ sửa file này (tên, email, link, dự án, kỹ năng...)
build.py             <- sinh website vào dist/
templates/           <- giao diện HTML (Jinja2)
static/              <- css, js, favicon, ảnh (assets/)
requirements.txt     <- Jinja2, Pillow
.github/workflows/   <- tự deploy lên GitHub Pages
dist/                <- kết quả build (không sửa tay)
```

## Chạy thử (Windows PowerShell)

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 build.py --serve
```

Mở http://localhost:8000. Sửa `config.py` rồi chạy lại lệnh trên để thấy thay đổi.
`py -3.12 build.py --check` chỉ kiểm tra cấu hình và in cảnh báo.

## Thay thông tin của bạn

Tất cả nằm trong `config.py`:

| Cần thay | Chỗ sửa |
|---|---|
| Tên, chức danh, email, giới thiệu | `PROFILE` |
| Ảnh đại diện | chép ảnh vào `static/assets/`, đặt `PROFILE["avatar"] = "assets/avatar.jpg"` |
| Facebook, YouTube, GitHub, LinkedIn, Blog | `LINKS` (điền `url`; để trống thì ẩn) |
| CV | chép PDF vào `static/assets/cv.pdf`, đặt `RESUME["url"] = "assets/cv.pdf"` (hoặc link https) |
| Dự án | `PROJECTS` (ảnh bìa trong `static/assets/`) |
| Kỹ năng, học vấn, kinh nghiệm | `SKILLS`, `ABOUT`, `EXPERIENCE` |
| Địa chỉ website | `SITE["url"]` hoặc biến môi trường `SITE_URL` |

Mục có `"example": True` là dữ liệu mẫu và hiện nhãn "Ví dụ". Thay nội dung thật rồi xoá dòng đó.

## Deploy (nhận đường dẫn công khai)

**GitHub Pages (miễn phí):**
1. Tạo repo GitHub, đẩy toàn bộ thư mục này lên nhánh `main`.
2. Repo → Settings → Pages → Source: **GitHub Actions**.
3. Workflow `.github/workflows/deploy.yml` tự build và đăng. Link dạng `https://<user>.github.io/<repo>/`.

**Netlify / Cloudflare Pages / Vercel:** Build command `pip install -r requirements.txt && python build.py`, output directory `dist`, đặt biến môi trường `SITE_URL` là địa chỉ công khai.

## Checklist thông tin cần thay

- [ ] `PROFILE`: họ tên, tên hiển thị, email, ảnh, giới thiệu, trạng thái sẵn sàng
- [ ] `LINKS`: URL thật của từng tài khoản
- [ ] `RESUME`: file CV thật
- [ ] `PROJECTS`: dự án thật (repo, demo, ảnh bìa), xoá dự án mẫu
- [ ] `SKILLS`: chỉ giữ công nghệ bạn thật sự dùng
- [ ] `ABOUT`: học vấn, mục tiêu, ngôn ngữ
- [ ] `EXPERIENCE`: thêm nếu có (rỗng thì mục tự ẩn)
- [ ] `SITE["url"]` hoặc `SITE_URL`
- [ ] Thay `static/favicon.svg` nếu muốn logo riêng

## Quyền riêng tư và tích hợp bên thứ ba

- Mặc định không cookie theo dõi, không analytics, không gửi dữ liệu đi đâu.
- Biểu mẫu liên hệ chỉ xuất hiện khi bạn đặt `SITE["contact_form_endpoint"]` (ví dụ Formspree). Không có endpoint thì chỉ có nút gửi email (mailto) và sao chép email, không giả vờ gửi tin.
- Analytics tuỳ chọn: Plausible (`SITE["analytics"]`), tải script từ plausible.io khi bật.
- Không công khai số điện thoại hay địa chỉ nhà.
- Mọi URL được kiểm tra (chỉ `http(s)`/`mailto`), liên kết ngoài có `rel="noopener noreferrer"`.

## Chưa làm (có thể thêm sau)

QR code của link công khai, trang chi tiết riêng cho từng dự án, ảnh OG thiết kế riêng, chống spam phía server cho form (cần backend).
