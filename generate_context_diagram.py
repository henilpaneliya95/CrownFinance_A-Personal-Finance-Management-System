from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1400, 900
BG = "white"
LINE = "black"

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)


def get_font(size=28, bold=False):
    # Prefer common Windows fonts; fall back to default if unavailable.
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def draw_centered_text(box, text, font, fill=LINE):
    x1, y1, x2, y2 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x1 + (x2 - x1 - tw) / 2
    ty = y1 + (y2 - y1 - th) / 2
    draw.multiline_text((tx, ty), text, font=font, fill=fill, align="center")


def arrow(start, end, label=None, label_offset=(0, 0), width=3):
    draw.line([start, end], fill=LINE, width=width)

    # Arrow head
    ex, ey = end
    sx, sy = start
    dx, dy = ex - sx, ey - sy
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    head_len = 16
    head_w = 8
    p1 = (ex, ey)
    p2 = (ex - ux * head_len + px * head_w, ey - uy * head_len + py * head_w)
    p3 = (ex - ux * head_len - px * head_w, ey - uy * head_len - py * head_w)
    draw.polygon([p1, p2, p3], fill=LINE)

    if label:
        mx = (sx + ex) / 2 + label_offset[0]
        my = (sy + ey) / 2 + label_offset[1]
        font = get_font(24, bold=True)
        bbox = draw.textbbox((mx, my), label, font=font)
        pad = 6
        draw.rectangle((bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad), fill="white")
        draw.text((mx, my), label, fill=LINE, font=font)


# Boxes
entity_font = get_font(42, bold=True)
small_font = get_font(32, bold=True)

user_box = (90, 350, 340, 500)
admin_box = (1060, 350, 1310, 500)
ai_box = (1040, 90, 1320, 240)

for box, label in [
    (user_box, "User"),
    (admin_box, "Admin"),
    (ai_box, "AI Engine"),
]:
    draw.rectangle(box, outline=LINE, width=4)
    draw_centered_text(box, label, entity_font)

# Central process (circle)
center = (700, 430)
radius = 150
cx, cy = center
proc_box = (cx - radius, cy - radius, cx + radius, cy + radius)
draw.ellipse(proc_box, outline=LINE, width=4)
draw_centered_text(proc_box, "Crown\nFinance", get_font(54, bold=True))

# Database cylinder
db_x1, db_y1, db_x2, db_y2 = 560, 650, 840, 820
oval_h = 34
draw.ellipse((db_x1, db_y1 - oval_h, db_x2, db_y1 + oval_h), outline=LINE, width=4)
draw.rectangle((db_x1, db_y1, db_x2, db_y2), outline=LINE, width=4)
draw.ellipse((db_x1, db_y2 - oval_h, db_x2, db_y2 + oval_h), outline=LINE, width=4)
draw_centered_text((db_x1, db_y1 + 30, db_x2, db_y2 - 20), "Finance\nDatabase", get_font(42, bold=True))

# Arrows and labels
# User <-> System
arrow((340, 390), (550, 400), "Register/Login,\nAdd transactions", (0, -55))
arrow((550, 470), (340, 460), "View dashboard,\nreports", (0, 20))

# Admin <-> System
arrow((1060, 400), (850, 410), "Manage users,\nsettings", (-10, -50))
arrow((850, 475), (1060, 470), "View system\nreports", (0, 20))

# AI Engine <-> System
arrow((1040, 210), (820, 320), "Send insight\nrequest", (-20, -45))
arrow((820, 340), (1040, 130), "Receive AI\nsuggestions", (0, -35))

# System <-> DB
arrow((670, 580), (670, 650), "Store data", (-120, 0))
arrow((730, 650), (730, 580), "Retrieve data", (20, 0))

# Title
draw.text((420, 30), "Context Flow Diagram - Crown Finance", font=get_font(44, bold=True), fill=LINE)

out_path = "image/crown_finance_context_flow.png"
img.save(out_path, "PNG")
print(f"Saved: {out_path}")
