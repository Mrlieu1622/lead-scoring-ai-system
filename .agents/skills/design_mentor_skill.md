# 🎨 TÀI LIỆU TIÊU CHUẨN THIẾT KẾ DASHBOARD HIỆN ĐẠI (DESIGN MENTOR SKILL)
*Tài liệu hướng dẫn & quy chuẩn thiết kế giao diện UI/UX cao cấp dành cho Dashboard được biên soạn bởi Design Mentor.*

---

## 1. Phong Cách Glassmorphism (Hiệu Ứng Kính Mờ)
Glassmorphism mang lại chiều sâu, cảm giác hiện đại và tính cao cấp cho giao diện Dashboard thông qua việc sử dụng các lớp layer bán trong suốt xếp chồng lên nhau.

### 📐 Quy chuẩn thông số kỹ thuật CSS:
*   **Background (Màu nền):** Sử dụng các gam màu có độ mờ nhẹ (Opacity từ `10%` đến `20%`).
    ```css
    background: rgba(255, 255, 255, 0.05); /* Cho Dark Mode */
    /* Hoặc */
    background: rgba(15, 23, 42, 0.4); /* Slate 900 với 40% Opacity */
    ```
*   **Backdrop Filter (Làm mờ hậu cảnh):** Đây là yếu tố cốt lõi của hiệu ứng kính mờ.
    ```css
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    ```
*   **Border (Đường viền kính):** Tạo hiệu ứng khúc xạ ánh sáng ở rìa thẻ bằng đường viền mỏng có độ trong suốt cao.
    ```css
    border: 1px solid rgba(255, 255, 255, 0.1);
    ```
*   **Box Shadow (Đổ bóng):** Sử dụng bóng đổ rất nhẹ và tỏa rộng để tách biệt thẻ kính với nền.
    ```css
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    ```
*   **Border Radius (Bo góc):** Khuyên dùng bo góc từ `16px` đến `24px` để tạo cảm giác mềm mại, hiện đại.

---

## 2. Tiêu Chuẩn Giao Diện Tối (Dark Mode)
Dark Mode của Dashboard hiện đại không đơn thuần là thay đổi màu nền sang đen tuyền `#000000`. Cần áp dụng quy tắc phân lớp độ sâu bằng màu sắc:

*   **Quy tắc phối màu nền:**
    *   **Nền chính (Workspace Background):** Sử dụng các tông màu tối sâu như Xanh đen, Xám đậm (Ví dụ: Slate 950 `#0b0f19` hoặc `#0f172a`).
    *   **Thẻ thông tin (Cards/Panels):** Áp dụng hiệu ứng Glassmorphism trên nền tối hơn nhẹ hoặc sáng hơn nhẹ để phân lớp trực quan (Ví dụ: `#1e293b` với opacity).
*   **Tránh dùng màu đen tuyệt đối (#000000):** Màu đen tuyệt đối gây mỏi mắt và làm mất đi các chi tiết bóng đổ đổ từ các lớp layer.
*   **Neon/Cyber Accents:** Sử dụng các đường line phát sáng hoặc màu sắc rực rỡ với sắc độ cao (Cyan, Emerald, Violet) để làm nổi bật các trạng thái quan trọng.
    ```css
    /* Hiệu ứng phát sáng nhẹ cho các phần tử tiêu điểm (glow effect) */
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
    ```

---

## 3. Phong Cách Bố Trí KPI (KPI Card Layout & Hierarchy)
KPI Cards là trung tâm thông tin của Dashboard. Thiết kế cần phân cấp thị giác cực kỳ rõ ràng để người dùng nắm bắt số liệu chỉ trong 1 giây.

### 📐 Cấu trúc bố cục chuẩn của một KPI Card:
1.  **Header:** Tiêu đề chỉ số (font size: `13px` - `14px`, màu chữ phụ hoặc độ mờ `60%`) kèm theo **Icon đại diện** nằm ở góc phải (sử dụng nền bo tròn đồng màu dạng mờ).
2.  **Body (Chỉ số chính):** Con số thống kê nổi bật nhất (font size: `28px` - `36px`, font-weight: `700`, màu trắng tinh hoặc màu nhấn chính).
3.  **Footer (Xu hướng biến động):**
    *   Tăng trưởng: Màu xanh lá cây (Emerald `#10b981`), kèm icon mũi tên hướng lên `↑`.
    *   Giảm sút: Màu đỏ (Rose `#f43f5e`), kèm icon mũi tên hướng xuống `↓`.
    *   Văn bản phụ: Khoảng thời gian so sánh (Ví dụ: *so với tháng trước* - màu chữ mờ `40%`).

```
+----------------------------------------+
| 💼 Tổng doanh thu            [ Icon ]  |
|                                        |
|  $128,450.00                           |
|                                        |
|  [↑ +12.5%] so với tháng trước         |
+----------------------------------------+
```

---

## 4. Nguyên Tắc Phối Màu Tương Phản (Contrast Color Coordination)
Màu sắc trong Dashboard thực hiện vai trò phân nhóm thông tin và truyền tải trạng thái nhanh chóng.

*   **Tỷ lệ phối màu 60-30-10:**
    *   `60%` Màu nền tối chủ đạo (Slate 950/900).
    *   `30%` Màu cấu trúc (Xám trung tính, Slate 800 cho sidebar, thẻ thông tin, bảng biểu).
    *   `10%` Màu nhấn (Accent color) như Cyan, Purple, Emerald cho nút bấm, biểu đồ, chỉ số quan trọng cần tương tác.
*   **Bảng màu Trạng thái (Semantic Colors) tương phản cao trên nền tối:**
    *   **Success (Thành công/Tăng):** Emerald Green (`#10b981`) tương phản mạnh với nền tối, tạo cảm giác an tâm.
    *   **Warning (Cảnh báo):** Amber Orange (`#f59e0b`) thu hút sự chú ý vừa phải.
    *   **Danger (Nguy hiểm/Giảm):** Rose Red (`#f43f5e`) nổi bật lập tức để báo động lỗi hoặc suy giảm.
    *   **Info (Thông tin):** Sky Blue (`#0ea5e9`) hoặc Indigo (`#6366f1`) thân thiện cho dữ liệu trung tính.
*   **Tiêu chuẩn tiếp cận (Accessibility):** Độ tương phản của chữ (Text) với nền tối phải đạt tỷ lệ tối thiểu **4.5:1** (theo chuẩn WCAG AA).

---

## 5. Hiệu Ứng Mượt Mà Khi Dữ Liệu Nhảy Số (Real-time Smooth Transitions)
Để mang lại cảm giác sống động (Real-time), dữ liệu số trên Dashboard không nên thay đổi đột ngột mà phải nhảy số mượt mà (Count-up) hoặc chuyển cảnh êm ái.

### 📐 Giải pháp kỹ thuật:

#### A. CSS Transitions cho các thẻ dữ liệu:
Sử dụng `transition` để các thay đổi về màu sắc, kích thước và bóng đổ diễn ra mượt mà trong khoảng `0.3s` đến `0.5s` với đường cong cubic-bezier.
```css
.kpi-card {
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.kpi-card:hover {
    transform: translateY(-4px);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
}
```

#### B. Hiệu ứng nhảy số bằng JavaScript (Count Up Animation):
Khi dữ liệu thay đổi, dùng một hàm JavaScript nhỏ để tăng dần từ số cũ lên số mới thay vì thay đổi trực tiếp:
```javascript
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        // Áp dụng easeOutQuad để số nhảy chậm dần khi gần đến đích
        const easeProgress = progress * (2 - progress);
        const currentValue = Math.floor(easeProgress * (end - start) + start);
        element.innerHTML = currentValue.toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Cách dùng:
// animateValue(document.getElementById("revenue-kpi"), 0, 128450, 1500);
```

#### C. CSS Keyframes cho hiệu ứng cập nhật dữ liệu (Pulse/Highlight):
Mỗi khi nhận được dữ liệu real-time mới, thêm class `.flash-update` vào thẻ hoặc số để tạo hiệu ứng phát sáng mờ rồi tắt dần, báo hiệu cho người dùng biết dữ liệu vừa được cập nhật thành công:
```css
@keyframes pulseGlow {
    0% {
        text-shadow: 0 0 0px rgba(16, 185, 129, 0);
        color: #10b981; /* Đổi màu tạm thời sang xanh khi update */
    }
    30% {
        text-shadow: 0 0 12px rgba(16, 185, 129, 0.8);
        color: #34d399;
    }
    100% {
        text-shadow: 0 0 0px rgba(16, 185, 129, 0);
        color: #ffffff;
    }
}

.flash-update {
    animation: pulseGlow 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}
```

---
*Design Mentor chúc bạn thiết kế được những sản phẩm Dashboard tuyệt vời và mang lại trải nghiệm WOW cho người dùng!*
