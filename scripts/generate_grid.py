import os
from PIL import Image, ImageDraw, ImageFont

def create_grid_overlay(image_path, output_path, step_percent=5):
    try:
        with Image.open(image_path) as img:
            # Convert to RGB to ensure we can draw colored lines (if it was indexed)
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img)
            width, height = img.size
            
            # Use default font or try to load one
            try:
                # Try loading a system font that is readable
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            except:
                font = ImageFont.load_default()

            # Draw Vertical Lines (X axis)
            for p in range(0, 101, step_percent):
                x = int((p / 100) * width)
                # Line
                color = "red" if p % 10 == 0 else "yellow"
                width_line = 2 if p % 10 == 0 else 1
                draw.line([(x, 0), (x, height)], fill=color, width=width_line)
                # Label
                if p % 10 == 0:
                     label = f"X:{p}"
                     # Draw text with outline for readability
                     draw.text((x + 5, 10), label, fill="white", font=font, stroke_width=2, stroke_fill="black")
                     draw.text((x + 5, height - 30), label, fill="white", font=font, stroke_width=2, stroke_fill="black")

            # Draw Horizontal Lines (Y axis)
            for p in range(0, 101, step_percent):
                y = int((p / 100) * height)
                # Line
                color = "red" if p % 10 == 0 else "yellow"
                width_line = 2 if p % 10 == 0 else 1
                draw.line([(0, y), (width, y)], fill=color, width=width_line)
                # Label
                if p % 10 == 0:
                     label = f"Y:{p}"
                     draw.text((10, y + 5), label, fill="white", font=font, stroke_width=2, stroke_fill="black")
                     draw.text((width - 60, y + 5), label, fill="white", font=font, stroke_width=2, stroke_fill="black")

            img.save(output_path)
            print(f"Grid map saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    source = "public/world_map.webp"
    dest = "src/assets/map/world_map_grid.jpg"
    create_grid_overlay(source, dest, step_percent=5)
