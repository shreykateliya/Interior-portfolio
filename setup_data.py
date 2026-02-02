import os
import django
from django.core.files import File
from django.conf import settings
from pathlib import Path

# --- 1. Define Base Directory (Fixes the error) ---
# This points to the folder containing manage.py
BASE_DIR = Path(__file__).resolve().parent

# --- 2. Setup Django Environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mistri_project.settings')
django.setup()

from showcase.models import Category, Project, ProjectImage

# --- Configuration ---
# Path where you saved the downloaded images
SOURCE_IMG_DIR = os.path.join(BASE_DIR, 'setup_images')

def run_setup():
    print("--- Starting MISTRI INTERIOR Data Setup ---")
    
    # Check if image folder exists
    if not os.path.exists(SOURCE_IMG_DIR):
        print(f"❌ Error: The folder '{SOURCE_IMG_DIR}' does not exist.")
        print("Please create a folder named 'setup_images' next to manage.py and add your images there.")
        return

    # Clear existing data to avoid duplicates (Optional - uncomment if you want to wipe old data)
    # Project.objects.all().delete()
    # Category.objects.all().delete()
    
    # 3. Create Categories
    cat_interior, _ = Category.objects.get_or_create(name="Interior Design", slug="interior-design")
    cat_furniture, _ = Category.objects.get_or_create(name="Bespoke Furniture", slug="bespoke-furniture")
    print("✅ Categories Created")

    # 4. Create Project 1: Living Room
    print("Creating Living Room Project...")
    living_proj, created = Project.objects.get_or_create(
        title="The Sharma Residence - Luxury Living",
        defaults={
            'category': cat_interior,
            'description': "A complete overhaul of a living space, focusing on warm tones, custom lighting, and a blend of modern Italian furniture with traditional accents.",
            'is_featured': True,
            'client_name': "Mr. & Mrs. Sharma"
        }
    )
    
    # Helper function to attach image safely
    def attach_image(obj, filename, is_main=False):
        file_path = os.path.join(SOURCE_IMG_DIR, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                if is_main:
                    obj.image.save(filename, File(f), save=True)
                else:
                    # Create new gallery image object
                    p_img = ProjectImage(project=obj)
                    p_img.image.save(filename, File(f), save=True)
            print(f"   - Attached: {filename}")
        else:
            print(f"   ⚠️ Warning: Image {filename} not found in setup_images folder.")

    # Attach Main Image
    attach_image(living_proj, 'living_main.jpg', is_main=True)
    
    # Attach Gallery Images
    gallery_imgs = ['living_1.jpg', 'living_2.jpg', 'living_3.jpg']
    for img_name in gallery_imgs:
        attach_image(living_proj, img_name)


    # 5. Create Project 2: Kitchen
    print("\nCreating Kitchen Project...")
    kitchen_proj, created = Project.objects.get_or_create(
        title="Sector 62 Modular Kitchen",
        defaults={
            'category': cat_interior,
            'description': "A high-gloss, handle-less modular kitchen designed for efficiency and style. Features quartz countertops and integrated appliances.",
            'is_featured': True
        }
    )
    attach_image(kitchen_proj, 'kitchen_main.jpg', is_main=True)
    
    gallery_imgs = ['kitchen_1.jpg', 'kitchen_2.jpg']
    for img_name in gallery_imgs:
        attach_image(kitchen_proj, img_name)
            
            
    # 6. Create Project 3: Bedroom Furniture
    print("\nCreating Bedroom Furniture Project...")
    bed_proj, created = Project.objects.get_or_create(
        title="Minimalist Teak Bed & Wardrobe",
        defaults={
            'category': cat_furniture,
            'description': "Custom designed bedroom furniture crafted from reclaimed teak wood. The design focuses on clean lines and hidden joinery.",
            'is_featured': False
        }
    )
    attach_image(bed_proj, 'bed_main.jpg', is_main=True)

    gallery_imgs = ['bed_1.jpg', 'bed_2.jpg']
    for img_name in gallery_imgs:
        attach_image(bed_proj, img_name)

    print("\n--- ✅ Setup Complete! Run 'python manage.py runserver' ---")

if __name__ == '__main__':
    run_setup()