from rembg import remove
from PIL import Image, ImageDraw
import io

def remove_background(image_bytes):
    """Menghapus background dari gambar mentah."""
    output_bytes = remove(image_bytes)
    return Image.open(io.BytesIO(output_bytes)).convert("RGBA")

def create_story_canvas(product_img, bg_style, logo_img=None):
    """Membuat kanvas 9:16 (1080x1920) dengan smart ratio locking."""
    # Ukuran standar Meta Ads / Reels
    canvas_w, canvas_h = 1080, 1920
    
    # 1. Siapkan Latar Belakang
    canvas = Image.new("RGBA", (canvas_w, canvas_h))
    draw = ImageDraw.Draw(canvas)
    
    if bg_style == "Minimalist White":
        canvas.paste((250, 250, 250, 255), [0, 0, canvas_w, canvas_h])
    elif bg_style == "Premium Dark":
        canvas.paste((20, 20, 20, 255), [0, 0, canvas_w, canvas_h])
    elif bg_style == "Vibrant Gradient":
        # Membuat gradient sederhana (Top to Bottom)
        for y in range(canvas_h):
            r = int(255 - (y / canvas_h) * 100)
            g = int(150 - (y / canvas_h) * 50)
            b = int(50 + (y / canvas_h) * 100)
            draw.line([(0, y), (canvas_w, y)], fill=(r, g, b, 255))
    else:
        canvas.paste((255, 255, 255, 255), [0, 0, canvas_w, canvas_h]) # Default

    # 2. Smart Ratio Lock (Resize produk tanpa distorsi)
    # Maksimal lebar produk di kanvas adalah 80% dari lebar kanvas
    max_w = int(canvas_w * 0.8)
    max_h = int(canvas_h * 0.6)
    
    prod_w, prod_h = product_img.size
    ratio = min(max_w / prod_w, max_h / prod_h)
    new_w, new_h = int(prod_w * ratio), int(prod_h * ratio)
    
    resized_product = product_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 3. Posisikan produk di tengah
    offset_x = (canvas_w - new_w) // 2
    offset_y = (canvas_h - new_h) // 2
    canvas.paste(resized_product, (offset_x, offset_y), resized_product)
    
    # 4. Tambahkan Watermark Logo (jika ada)
    if logo_img:
        logo_w, logo_h = logo_img.size
        # Resize logo menjadi kecil (max lebar 200px)
        l_ratio = 200 / logo_w
        logo_new_w, logo_new_h = int(logo_w * l_ratio), int(logo_h * l_ratio)
        resized_logo = logo_img.resize((logo_new_w, logo_new_h), Image.Resampling.LANCZOS).convert("RGBA")
        
        # Posisikan di pojok kanan atas
        logo_x = canvas_w - logo_new_w - 50
        logo_y = 50
        canvas.paste(resized_logo, (logo_x, logo_y), resized_logo)

    return canvas.convert("RGB")
