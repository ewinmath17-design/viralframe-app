from rembg import remove
from PIL import Image, ImageDraw, ImageOps
import io

def remove_background(image_bytes):
    """Menghapus background dengan memperbaiki orientasi HP (EXIF) terlebih dahulu."""
    # 1. Buka gambar dan perbaiki rotasi otomatis dari kamera HP
    raw_img = Image.open(io.BytesIO(image_bytes))
    raw_img = ImageOps.exif_transpose(raw_img)
    
    # 2. Konversi kembali ke bytes untuk diproses rembg
    img_byte_arr = io.BytesIO()
    raw_img.save(img_byte_arr, format='PNG')
    fixed_bytes = img_byte_arr.getvalue()
    
    # 3. Hapus background
    output_bytes = remove(fixed_bytes)
    return Image.open(io.BytesIO(output_bytes)).convert("RGBA")

def create_story_canvas(product_img, bg_style, logo_img=None):
    """Membuat kanvas 9:16 (1080x1920) dengan smart ratio locking."""
    canvas_w, canvas_h = 1080, 1920
    canvas = Image.new("RGBA", (canvas_w, canvas_h))
    draw = ImageDraw.Draw(canvas)
    
    if bg_style == "Minimalist White":
        canvas.paste((250, 250, 250, 255), [0, 0, canvas_w, canvas_h])
    elif bg_style == "Premium Dark":
        canvas.paste((20, 20, 20, 255), [0, 0, canvas_w, canvas_h])
    elif bg_style == "Vibrant Gradient":
        for y in range(canvas_h):
            r = int(255 - (y / canvas_h) * 100)
            g = int(150 - (y / canvas_h) * 50)
            b = int(50 + (y / canvas_h) * 100)
            draw.line([(0, y), (canvas_w, y)], fill=(r, g, b, 255))
    else:
        canvas.paste((255, 255, 255, 255), [0, 0, canvas_w, canvas_h])

    # Pastikan aspect ratio produk terkunci kuat (TIDAK GEPENG)
    prod_w, prod_h = product_img.size
    max_w = int(canvas_w * 0.8)
    max_h = int(canvas_h * 0.6)
    
    ratio = min(max_w / prod_w, max_h / prod_h)
    new_w = int(prod_w * ratio)
    new_h = int(prod_h * ratio)
    
    resized_product = product_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Posisikan persis di tengah
    offset_x = (canvas_w - new_w) // 2
    offset_y = (canvas_h - new_h) // 2
    
    # Gunakan gambar itu sendiri sebagai mask agar transparansi background rapi
    canvas.paste(resized_product, (offset_x, offset_y), resized_product)
    
    # Tambahkan Logo jika ada
    if logo_img:
        logo_img = ImageOps.exif_transpose(logo_img) # Fix rotasi logo juga
        logo_w, logo_h = logo_img.size
        l_ratio = 200 / logo_w
        logo_new_w = int(logo_w * l_ratio)
        logo_new_h = int(logo_h * l_ratio)
        resized_logo = logo_img.resize((logo_new_w, logo_new_h), Image.Resampling.LANCZOS).convert("RGBA")
        
        logo_x = canvas_w - logo_new_w - 50
        logo_y = 50
        canvas.paste(resized_logo, (logo_x, logo_y), resized_logo)

    # Ubah ke RGB murni agar engine video tidak error
    return canvas.convert("RGB")
