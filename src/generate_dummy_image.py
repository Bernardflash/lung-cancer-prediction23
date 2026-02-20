
from PIL import Image, ImageDraw
import os

# Create dummy image
img = Image.new('RGB', (150, 150), color='black')
d = ImageDraw.Draw(img)
d.ellipse((25, 25, 125, 125), fill='gray')
d.ellipse((60, 60, 90, 90), fill='white')

# Save
if not os.path.exists('data'):
    os.makedirs('data')
img.save('data/sample_ct_scan.jpg')
print("Dummy CT scan image saved to data/sample_ct_scan.jpg")
