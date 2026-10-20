"""
=====================================================================
  CẤU HÌNH DUY NHẤT CỦA WEBSITE  (chỉ cần sửa file này)
=====================================================================

Cách dùng:
  1. Sửa các giá trị bên dưới (tên, email, link mạng xã hội, dự án...).
  2. Chạy:  python build.py
  3. Thư mục `dist/` chứa website hoàn chỉnh để đưa lên hosting.

Quy ước:
  - Chuỗi rỗng ""  = chưa cấu hình  -> mục đó tự ẩn hoặc hiện thông báo "chưa cấu hình".
  - Văn bản hai ngôn ngữ dùng tr("tiếng Việt", "English").
    Nếu bạn chỉ muốn một ngôn ngữ, cứ viết chuỗi thường, ví dụ "Hà Nội".
  - Mục có `"example": True` là DỮ LIỆU MẪU, website sẽ hiện nhãn "Ví dụ".
    Hãy thay bằng thông tin thật rồi đổi/xoá `example`.
  - KHÔNG bịa thông tin. Không có thì để trống.
"""

from __future__ import annotations


def tr(vi: str, en: str) -> dict[str, str]:
    """Văn bản song ngữ."""
    return {"vi": vi, "en": en}


# ---------------------------------------------------------------------
# 1. WEBSITE
# ---------------------------------------------------------------------
SITE = {
    # Địa chỉ công khai, ví dụ "https://ten-cua-ban.github.io" hoặc "https://tenban.dev".
    # Cũng có thể đặt bằng biến môi trường SITE_URL khi build (ưu tiên hơn giá trị này).
    # Để trống thì sẽ KHÔNG tạo canonical / sitemap / og:url (không đoán localhost).
    "url": "",
    "default_lang": "vi",          # ngôn ngữ mặc định (đặt ở thư mục gốc)
    "languages": ["vi", "en"],     # ["vi"] nếu chỉ cần một ngôn ngữ
    "default_theme": "dark",       # "dark" | "light" | "system"
    "accent": "#4f7cff",           # màu theme-color cho trình duyệt di động
    # Phân tích truy cập thân thiện quyền riêng tư (mặc định TẮT).
    # Ví dụ Plausible: {"provider": "plausible", "domain": "tenban.dev"}
    "analytics": {"provider": "", "domain": ""},
    # Biểu mẫu liên hệ (mặc định TẮT). Dán endpoint thật, ví dụ Formspree:
    # "https://formspree.io/f/xxxxxxx". Để trống thì chỉ dùng mailto/sao chép email.
    "contact_form_endpoint": "",
    # Tạo file danh bạ .vcf để người xem lưu liên hệ (cần có email).
    "enable_vcard": True,
}

# ---------------------------------------------------------------------
# 2. HỒ SƠ CÁ NHÂN
# ---------------------------------------------------------------------
PROFILE = {
    "full_name": "Trương Đưc Hoan",        # TODO: thay bằng tên thật
    "display_name": "HOAN",          # TODO: tên ngắn dùng ở logo/footer
    "title": "Full-Stack Developer | AI Enthusiast",
    # Ảnh đại diện: đặt file vào static/assets/ rồi ghi "assets/avatar.jpg".
    # Để trống sẽ hiện avatar chữ cái đầu.
    "avatar": "",
    "avatar_alt": tr("Ảnh đại diện", "Profile photo"),
    "email": "truongduchoan116@gmail.com",                             # TODO: ví dụ "ban@example.com"
    "intro": tr(
        "Chào bạn. Bạn cần gì ở mình.",
    ),
    "focus": [
        tr("Mua/bán acc Liên Quân", "làm chung sức"),
    ],
    # Trạng thái sẵn sàng. status: "open" | "busy" | "closed" | "" (ẩn)
    "availability": {
        "status": "open",
        "label": tr("Đang tìm cơ hội thực tập", "Open to internship opportunities"),
    },                    # bỏ dòng này khi đã điền thông tin thật
}

# ---------------------------------------------------------------------
# 3. GIỚI THIỆU
# ---------------------------------------------------------------------
ABOUT = {
    "summary": tr(
        "Đây là đoạn giới thiệu mẫu. Hãy viết 2-4 câu về bản thân, nền tảng học tập "
        "và điều bạn muốn làm.",
        "This is a sample introduction. Write 2-4 sentences about yourself, your "
        "background and what you want to do.",
    ),
    "education": [
        {
            "institution": tr("Tên trường đại học", "University name"),
            "qualification": tr("Khoa học Máy tính", "Computer Science"),
            "dates": "",
        },
    ],
    "interests": [tr("Phát triển web", "Web development"), tr("Trí tuệ nhân tạo", "Artificial intelligence")],
    "goals": tr("Mục tiêu nghề nghiệp của bạn.", "Your professional goals."),
    "philosophy": tr("Triết lý làm việc của bạn.", "Your working philosophy."),
    # Chỉ ghi ngôn ngữ và mức độ bạn thực sự có.
    "languages": [{"name": tr("Tiếng Việt", "Vietnamese"), "level": tr("Bản ngữ", "Native")}],
    "learning": [tr("Điều bạn đang học hiện tại.", "What you are currently learning.")],
    "example": True,
}

# ---------------------------------------------------------------------
# 4. LIÊN KẾT MẠNG XÃ HỘI
#    url để trống = ẩn. Chỉ nhận http(s):// hoặc mailto:
#    icon: github | facebook | youtube | linkedin | mail | link | file
# ---------------------------------------------------------------------
LINKS = [
    {"id": "github", "platform": "GitHub", "icon": "github", "url": "",
     "description": tr("Mã nguồn và dự án", "Source code and projects"),
     "custom_label": "", "visible": True, "order": 1, "new_tab": True},
    {"id": "linkedin", "platform": "LinkedIn", "icon": "linkedin", "url": "",
     "description": tr("Hồ sơ nghề nghiệp", "Professional profile"),
     "custom_label": "", "visible": True, "order": 2, "new_tab": True},
    {"id": "facebook", "platform": "Facebook", "icon": "facebook", "url": "https://www.facebook.com/hoancubu100cm?locale=vi_VN",
     "description": tr("Kết nối cá nhân", "Personal connection"),
     "custom_label": "", "visible": True, "order": 3, "new_tab": True},
    {"id": "youtube", "platform": "YouTube", "icon": "youtube", "url": "https://www.youtube.com/results?search_query=dh+thao+tac+tay",
     "description": tr("Video và bài giảng", "Videos and talks"),
     "custom_label": "", "visible": True, "order": 4, "new_tab": True},
    {"id": "blog", "platform": "Blog", "icon": "link", "url": "",
     "description": tr("Bài viết cá nhân", "Personal writing"),
     "custom_label": "", "visible": True, "order": 5, "new_tab": True},
    # Muốn thêm nền tảng khác: sao chép một khối ở trên và đổi nội dung.
]

# ---------------------------------------------------------------------
# 5. CV / RESUME
#    Cách 1: đặt file PDF vào static/assets/ và ghi "assets/cv.pdf"
#    Cách 2: dán link https:// (Google Drive, v.v.)
#    Để trống: nút CV hiện thông báo "chưa cấu hình" thay vì tải file giả.
# ---------------------------------------------------------------------
RESUME = {"url": "", "download_name": "CV.pdf"}

# ---------------------------------------------------------------------
# 6. DỰ ÁN NỔI BẬT  (sắp xếp theo `order`)
#    status: "completed" | "in_progress" | "planned"
#    cover: "assets/ten-anh.png" trong static/, để trống thì dùng ảnh nền mặc định
# ---------------------------------------------------------------------
PROJECTS = [
    {
        "id": "sample-project",
        "name": tr("Dự án mẫu", "Sample project"),
        "description": tr(
            "Mô tả ngắn gọn dự án: giải quyết vấn đề gì, dành cho ai.",
            "Short description: what problem it solves and for whom.",
        ),
        "category": "web",   # dùng cho bộ lọc: web | ai | tool | ... (tự đặt)
        "stack": ["Python"],
        "cover": "",
        "repo_url": "",
        "demo_url": "",
        "status": "in_progress",
        "role": tr("Vai trò và đóng góp của bạn.", "Your role and contributions."),
        "features": [tr("Tính năng chính 1", "Key feature 1")],
        "order": 1,
        "example": True,
    },
]

# Tên hiển thị của các nhóm dự án (dùng cho bộ lọc)
PROJECT_CATEGORIES = {
    "web": tr("Web", "Web"),
    "ai": tr("AI / ML", "AI / ML"),
    "tool": tr("Công cụ", "Tools"),
}

# ---------------------------------------------------------------------
# 7. KỸ NĂNG  (chỉ liệt kê tên, KHÔNG có điểm số/số năm kinh nghiệm)
#    Danh sách dưới đây là MẪU: hãy xoá những gì bạn chưa dùng.
# ---------------------------------------------------------------------
SKILLS = {
    "example": True,
    "groups": [
        {"name": tr("Ngôn ngữ lập trình", "Programming languages"), "items": ["Python", "JavaScript", "TypeScript"]},
        {"name": tr("Frontend", "Frontend"), "items": ["HTML", "CSS", "React"]},
        {"name": tr("Backend", "Backend"), "items": ["FastAPI", "Node.js"]},
        {"name": tr("Cơ sở dữ liệu", "Databases"), "items": ["PostgreSQL", "SQLite"]},
        {"name": tr("AI / Machine Learning", "AI / Machine Learning"), "items": ["TensorFlow", "scikit-learn"]},
        {"name": tr("Công cụ & hạ tầng", "Tools & infrastructure"), "items": ["Git", "Docker", "Linux"]},
    ],
}

# ---------------------------------------------------------------------
# 8. KINH NGHIỆM (thực tập, việc làm, nghiên cứu, hoạt động)
#    Để danh sách rỗng thì cả mục tự ẩn. Không bịa kinh nghiệm.
# ---------------------------------------------------------------------
EXPERIENCE: list[dict] = [
    # {
    #     "organization": "Tên tổ chức",
    #     "role": tr("Vị trí", "Role"),
    #     "dates": "06/2026 – 09/2026",
    #     "description": tr("Mô tả công việc.", "What you did."),
    #     "project_id": "",   # id dự án liên quan (tuỳ chọn)
    # },
]

# ---------------------------------------------------------------------
# 9. CHỮ TRÊN GIAO DIỆN (hai ngôn ngữ)
# ---------------------------------------------------------------------
UI = {
    "vi": {
        "skip": "Bỏ qua đến nội dung chính",
        "nav_about": "Giới thiệu", "nav_projects": "Dự án", "nav_skills": "Kỹ năng",
        "nav_experience": "Kinh nghiệm", "nav_links": "Liên kết", "nav_contact": "Liên hệ",
        "menu_open": "Mở menu", "menu_close": "Đóng menu",
        "theme_toggle": "Đổi giao diện sáng/tối",
        "lang_switch": "English", "lang_switch_label": "Switch to English",
        "cta_contact": "Liên hệ", "cta_projects": "Xem dự án", "cta_resume": "Tải CV",
        "resume_missing": "CV chưa được cấu hình",
        "example_badge": "Ví dụ",
        "example_note": "Nội dung mẫu, hãy thay bằng thông tin thật trong config.py.",
        "about_title": "Giới thiệu", "education": "Học vấn", "interests": "Quan tâm kỹ thuật",
        "goals": "Mục tiêu nghề nghiệp", "philosophy": "Triết lý làm việc",
        "languages": "Ngôn ngữ", "learning": "Đang học", "more_details": "Xem chi tiết",
        "links_title": "Liên kết", "links_lead": "Tất cả tài khoản của mình ở một nơi.",
        "link_not_set": "Chưa cấu hình",
        "projects_title": "Dự án nổi bật", "search_projects": "Tìm dự án",
        "filter_all": "Tất cả", "no_projects": "Không có dự án phù hợp.",
        "role": "Vai trò", "features": "Tính năng", "repo": "Mã nguồn", "demo": "Demo",
        "status_completed": "Hoàn thành", "status_in_progress": "Đang thực hiện", "status_planned": "Dự kiến",
        "skills_title": "Kỹ năng & công nghệ",
        "experience_title": "Kinh nghiệm",
        "contact_title": "Liên hệ", "contact_lead": "Rất vui được kết nối về cơ hội thực tập, dự án hoặc hợp tác.",
        "email_me": "Gửi email", "copy_email": "Sao chép email", "copied": "Đã sao chép",
        "copy_failed": "Không sao chép được, hãy chọn và sao chép thủ công.",
        "email_missing": "Email chưa được cấu hình.",
        "share": "Chia sẻ trang", "share_copied": "Đã sao chép liên kết trang",
        "save_contact": "Lưu danh bạ (.vcf)",
        "form_name": "Họ tên", "form_email": "Email của bạn", "form_message": "Nội dung",
        "form_send": "Gửi tin nhắn", "form_sending": "Đang gửi...",
        "form_success": "Đã gửi tin nhắn. Cảm ơn bạn!",
        "form_error": "Gửi không thành công. Vui lòng thử lại hoặc dùng email.",
        "err_required": "Trường này là bắt buộc.", "err_email": "Email không hợp lệ.",
        "err_short": "Nội dung quá ngắn (tối thiểu 10 ký tự).",
        "back_to_top": "Về đầu trang", "updated": "Cập nhật lần cuối",
        "privacy": "Trang này không dùng cookie theo dõi và không thu thập dữ liệu cá nhân khi chưa bật phân tích.",
        "err_404_title": "Không tìm thấy trang", "err_404_text": "Trang bạn tìm không tồn tại hoặc đã được chuyển.",
        "err_404_back": "Về trang chủ",
        "noscript": "Một số tính năng (đổi giao diện, lọc dự án, sao chép) cần bật JavaScript.",
    },
    "en": {
        "skip": "Skip to main content",
        "nav_about": "About", "nav_projects": "Projects", "nav_skills": "Skills",
        "nav_experience": "Experience", "nav_links": "Links", "nav_contact": "Contact",
        "menu_open": "Open menu", "menu_close": "Close menu",
        "theme_toggle": "Toggle light/dark theme",
        "lang_switch": "Tiếng Việt", "lang_switch_label": "Chuyển sang tiếng Việt",
        "cta_contact": "Contact me", "cta_projects": "View projects", "cta_resume": "Download CV",
        "resume_missing": "Resume not configured",
        "example_badge": "Example",
        "example_note": "Sample content, replace it with real information in config.py.",
        "about_title": "About me", "education": "Education", "interests": "Technical interests",
        "goals": "Professional goals", "philosophy": "Working philosophy",
        "languages": "Languages", "learning": "Currently learning", "more_details": "Show details",
        "links_title": "Links", "links_lead": "All my accounts in one place.",
        "link_not_set": "Not configured",
        "projects_title": "Featured projects", "search_projects": "Search projects",
        "filter_all": "All", "no_projects": "No matching projects.",
        "role": "Role", "features": "Features", "repo": "Source code", "demo": "Live demo",
        "status_completed": "Completed", "status_in_progress": "In progress", "status_planned": "Planned",
        "skills_title": "Skills & technologies",
        "experience_title": "Experience",
        "contact_title": "Contact", "contact_lead": "Happy to connect about internships, projects or collaboration.",
        "email_me": "Send email", "copy_email": "Copy email", "copied": "Copied",
        "copy_failed": "Could not copy, please select and copy manually.",
        "email_missing": "Email is not configured.",
        "share": "Share page", "share_copied": "Page link copied",
        "save_contact": "Save contact (.vcf)",
        "form_name": "Name", "form_email": "Your email", "form_message": "Message",
        "form_send": "Send message", "form_sending": "Sending...",
        "form_success": "Message sent. Thank you!",
        "form_error": "Could not send. Please try again or use email.",
        "err_required": "This field is required.", "err_email": "Invalid email address.",
        "err_short": "Message is too short (minimum 10 characters).",
        "back_to_top": "Back to top", "updated": "Last updated",
        "privacy": "This page uses no tracking cookies and collects no personal data unless analytics is enabled.",
        "err_404_title": "Page not found", "err_404_text": "The page you are looking for does not exist or has moved.",
        "err_404_back": "Back to home",
        "noscript": "Some features (theme, project filter, copy) need JavaScript.",
    },
}
