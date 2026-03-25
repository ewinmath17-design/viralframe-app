import numpy as np
from moviepy.editor import VideoClip
from PIL import Image
import tempfile

def create_ken_burns_video(pil_image, duration=3):
    """Membuat video MP4 3 detik dengan efek zoom in perlahan dari gambar statis."""
    w, h = pil_image.size

    def make_frame(t):
        # Hitung skala zoom berdasarkan waktu (zoom in maksimal 10%)
        scale = 1.0 + (0.1 * (t / duration))
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize gambar
        resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Crop kembali ke ukuran tengah persis (WAJIB Integer)
        left = int((new_w - w) / 2)
        top = int((new_h - h) / 2)
        cropped = resized.crop((left, top, left + w, top + h))
        
        return np.array(cropped)

    # Buat klip video
    clip = VideoClip(make_frame, duration=duration)
    
    # Simpan ke temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    
    # Render (fps 24 cukup)
    clip.write_videofile(temp_file.name, fps=24, codec="libx264", audio=False, logger=None)
    
    return temp_file.name
