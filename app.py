import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

# Global variable to hold the image to save
image_to_save = None

def resize_and_center_image(original_image):
    original_width, original_height = original_image.size
    target_size = 200
    new_image = Image.new("RGB", (target_size, target_size), color='white')

    if original_width > original_height:
        new_height = int(target_size * original_height / original_width)
        resized_image = original_image.resize((target_size, new_height), Image.LANCZOS)
    else:
        new_width = int(target_size * original_width / original_height)
        resized_image = original_image.resize((new_width, target_size), Image.LANCZOS)

    x = (target_size - resized_image.size[0]) // 2
    y = (target_size - resized_image.size[1]) // 2

    new_image.paste(resized_image, (x, y))
    return new_image

def log_message(message):
    log_area.config(state='normal')
    log_area.insert(tk.END, message + "\n")
    log_area.yview(tk.END)
    log_area.config(state='disabled')

def select_image():
    file_types = [
        ('Bilddateien', '*.png;*.jpg;*.jpeg;*.gif;*.bmp'),
        ('Alle Dateien', '*.*')
    ]
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        log_message("Bild ausgewählt: " + file_path)
        try:
            global image_to_save
            original_image = Image.open(file_path)
            image_to_save = resize_and_center_image(original_image)
            img = ImageTk.PhotoImage(image_to_save)
            panel.configure(image=img)
            panel.image = img
            save_button.config(state="normal")
            log_message("Bild wurde konvertiert und ist bereit zum Speichern.")
        except Exception as e:
            messagebox.showerror("Fehler", "Fehler beim Öffnen des Bildes: " + str(e))
            log_message("Fehler beim Konvertieren des Bildes.")

def save_image():
    global image_to_save
    if image_to_save:
        file_types = [
            ('JPEG', '*.jpg'),
            ('PNG', '*.png'),
            ('Alle Dateien', '*.*')
        ]
        save_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension=".jpg")
        if save_path:
            if image_to_save.mode == "RGBA":
                image_to_save = image_to_save.convert("RGB")
            image_to_save.save(save_path, "JPEG")
            messagebox.showinfo("Erfolg", "Bild erfolgreich gespeichert!")
            log_message("Bild gespeichert: " + save_path)
    else:
        messagebox.showwarning("Warnung", "Es gibt kein Bild zum Speichern.")

app = tk.Tk()
app.title("Bildkonverter-Tool")
app.geometry('600x700')

frame = tk.Frame(app)
frame.pack(pady=20)

label = tk.Label(frame, text="Bildkonverter-Tool", font=('Helvetica', 16))
label.pack()

select_button = tk.Button(frame, text="Bild auswählen", command=select_image)
select_button.pack(pady=5)

panel = tk.Label(frame)
panel.pack(pady=10)

save_button = tk.Button(frame, text="Konvertiertes Bild speichern", command=save_image, state="disabled")
save_button.pack(pady=5)

log_area = scrolledtext.ScrolledText(app, width=70, height=10, state='disabled')
log_area.pack(pady=10)

app.mainloop()
