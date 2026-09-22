from PIL import Image, ImageDraw, ImageFont
import random

# Load original image and resize to keep GIF size manageable
try:
    base_img = Image.open('assets/hero_banner_hq.jpg').convert('RGBA')
    base_img = base_img.resize((800, 450), Image.Resampling.LANCZOS)
except Exception as e:
    print(f"Error loading image: {e}")
    exit(1)

width, height = base_img.size

# Setup frames
frames = []
num_frames = 20
scanline_height = 100

# Setup matrix rain
chars = "0101#@!$*^%&ABCDEFGHIJKLMNOPQRSTUVWXYZ"
columns = 15
font_size = 14
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

matrix_drops = []
for _ in range(columns):
    x = random.randint(0, width - 20)
    y = random.randint(-400, 0)
    speed = random.randint(10, 30)
    col_chars = [random.choice(chars) for _ in range(20)]
    matrix_drops.append({'x': x, 'y': y, 'speed': speed, 'chars': col_chars})

for i in range(num_frames):
    # Create a fresh copy of the base image for this frame
    frame = base_img.copy()
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. Draw Matrix Rain
    for drop in matrix_drops:
        curr_y = drop['y']
        for char in drop['chars']:
            draw.text((drop['x'], curr_y), char, font=font, fill=(0, 255, 65, 180))
            curr_y += font_size
        
        # Move drop down
        drop['y'] += drop['speed']
        # Reset if off screen
        if drop['y'] > height:
            drop['y'] = random.randint(-400, -100)
            drop['x'] = random.randint(0, width - 20)
            
    # 2. Draw CRT Scanline
    scan_y = int((i / num_frames) * height)
    draw.rectangle([0, scan_y, width, scan_y + scanline_height], fill=(0, 255, 65, 30))
    draw.line([(0, scan_y), (width, scan_y)], fill=(57, 255, 20, 150), width=2)
    
    # Combine frame and overlay
    frame = Image.alpha_composite(frame, overlay)
    
    # Flicker effect (darken random frames slightly)
    if i % 5 == 0:
        dark_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 50))
        frame = Image.alpha_composite(frame, dark_overlay)
        
    frames.append(frame.convert('RGB'))

# Save as GIF
print("Saving GIF...")
frames[0].save(
    'assets/hero_banner_hq_animated.gif',
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    optimize=True
)
print("GIF created successfully!")
