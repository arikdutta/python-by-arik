import random
import sys
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io

PASSWORD = "python"
MAX_ATTEMPTS = 3

def ask_password():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pwd = input("Please enter the password: ")
        attempts += 1
        if pwd == PASSWORD:
            print("Password correct. Proceeding to image captcha...")
            return True
        remaining = MAX_ATTEMPTS - attempts
        if remaining:
            print(f"Incorrect password. {remaining} attempt(s) left.")
    print("Access denied! No more attempts.")
    return False

def create_label_image(text, size=(200, 120), bgcolor=(240,240,240), fg=(20,20,20)):
    img = Image.new("RGB", size, bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    w, h = draw.textsize(text, font=font)
    draw.text(((size[0]-w)/2, (size[1]-h)/2), text, fill=fg, font=font)
    return img

def run_image_captcha():
    # Define possible items and pick a target
    items = ["Cat", "Dog", "Car", "Tree", "Apple", "Boat"]
    # pick three distinct items to show
    choices = random.sample(items, 3)
    target = random.choice(choices)

    # Build a small GUI where user must click the image that matches the prompt
    root = tk.Tk()
    root.title("Image Captcha")
    prompt = tk.Label(root, text=f"Click the image that shows: {target}", font=("Arial", 14))
    prompt.pack(pady=8)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    result = {"success": False, "clicked": None}

    photos = []
    def on_click(choice):
        result["clicked"] = choice
        result["success"] = (choice == target)
        root.destroy()

    for choice in choices:
        img = create_label_image(choice)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        photo = ImageTk.PhotoImage(Image.open(bio))
        photos.append(photo)  # keep reference
        btn = tk.Button(frame, image=photo, command=lambda c=choice: on_click(c))
        btn.pack(side="left", padx=6)

    # Center window on screen
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()
    return result["success"], result["clicked"], target

def fallback_text_captcha():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    try:
        ans = int(input(f"Solve captcha to continue: {a} + {b} = "))
    except ValueError:
        return False
    return ans == (a + b)

def main():
    if not ask_password():
        return

    # Try to run image captcha; if GUI can't be created, fall back to numeric captcha
    try:
        success, clicked, target = run_image_captcha()
        if success:
            print("Captcha verified. Access granted!")
        else:
            print(f"Incorrect captcha selection ({clicked}). Access denied!")
    except Exception as e:
        print("Image captcha unavailable, falling back to numeric captcha.")
        if fallback_text_captcha():
            print("Captcha verified. Access granted!")
        else:
            print("Incorrect captcha. Access denied!")

if __name__ == "__main__":
    main()
