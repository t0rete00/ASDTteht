import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import winsound
import threading

class TomatoThrowGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tomato Throwing Game")
        self.root.geometry("800x600")

        # Pisteet
        self.scores = {"Kernesti": 0, "Ernesti": 0}
        self.lead = None

        # Kuvat
        self.kernesti_img = self.load_image("C:/Users/Terhi/Desktop/OAMK/3. vuosi/Advanced Software/kerne.png", (100, 100))
        self.ernesti_img = self.load_image("C:/Users/Terhi/Desktop/OAMK/3. vuosi/Advanced Software/erne.png", (100, 100))
        self.target_img = self.load_image("C:/Users/Terhi/Desktop/OAMK/3. vuosi/Advanced Software/maalitaulu.png", (200, 200))
        self.tomato_img = self.load_image("C:/Users/Terhi/Desktop/OAMK/3. vuosi/Advanced Software/tomato.png", (30, 30))
        self.splat_img = self.load_image("C:/Users/Terhi/Desktop/OAMK/3. vuosi/Advanced Software/splat.png", (50, 50))

        # UI:n rakentaminen
        self.build_ui()

    def load_image(self, path, size):
        try:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Failed to load image at {path}: {e}")
            return None

    def build_ui(self):
        # Kernesti vasemmalle reunalle
        self.kernesti_label = tk.Label(self.root, image=self.kernesti_img)
        x=0
        y=random.randint(0, 500)
        self.kernesti_label.place(x=x, y=y)

        # Maalitaulu keskelle
        self.target_label = tk.Label(self.root, image=self.target_img)
        x=400-100
        y=300-100
        self.target_label.place(x=x, y=y)

        # Ernesti oikealle reunalle
        self.ernesti_move_btn = tk.Button(self.root, text="Move Ernesti", command=self.move_ernesti)
        self.ernesti_move_btn.pack()
        self.ernesti_label = tk.Label(self.root, image=self.ernesti_img)
        x=800-100
        y=random.randint(0, 500)
        self.ernesti_label.place(x=x, y=y)

        # Heittopainikkeet
        self.throw_kernesti = tk.Button(self.root, text="Kernesti heittää", command=lambda: self.throw_tomato("Kernesti"))
        self.throw_kernesti.pack()
        self.throw_ernesti = tk.Button(self.root, text="Ernesti heittää", command=lambda: self.throw_tomato("Ernesti"))
        self.throw_ernesti.pack()

        # Tulokset
        self.score_display = tk.Label(self.root, text="Kernesti: 0 | Ernesti: 0")
        self.score_display.pack()

        # Reset-painike
        self.reset_btn = tk.Button(self.root, text="Reset Scores", command=self.reset_scores)
        self.reset_btn.pack()

    def move_ernesti(self):
        self.ernesti_label.place(x=700, y=random.randint(0, 500))

    def throw_tomato(self, thrower):
        if thrower == "Ernesti":
            start_x = 700
            start_y = self.ernesti_label.winfo_y() + self.ernesti_img.height() // 2
            direction = -1
        elif thrower == "Kernesti":
            start_x = 0
            start_y = self.kernesti_label.winfo_y() + self.kernesti_img.height() // 2
            direction = 1
        else:
            return
    
        tomato = tk.Label(self.root, image=self.tomato_img)
        tomato.place(x=start_x, y=start_y)

        # Create a splat label but don't place it yet
        splat = tk.Label(self.root, image=self.splat_img)
        
        def move_tomato():
            current_x = tomato.winfo_x()
            current_y = tomato.winfo_y()
            if current_x != 400:  # Move towards the target
                new_x = current_x + 5 * direction
                new_y = start_y - (400 - new_x) * 0.2  # This creates the arc
                tomato.place(x=new_x, y=new_y)
                if new_x != 400:
                    self.root.after(20, move_tomato)
                else:
                    tomato.destroy()
                    winsound.Beep(440, 100)  # Sound for tomato flight
                    self.check_hit(new_x, new_y)
            else:
                tomato.destroy()
                # Here we check if we should show the splat
                self.show_splat(new_x, new_y, splat)

        def show_splat(x, y, splat_label):
            target_x, target_y = self.target_label.winfo_x(), self.target_label.winfo_y()
            # Check if the tomato is close enough to the target to warrant a splat
            if (target_x - 50 < x < target_x + 200) and (target_y - 50 < y < target_y + 200):
                splat_label.place(x=target_x + 75, y=target_y + 75)  # Place splat at the center of the target
                # Optionally, remove the splat after a short time
                self.root.after(1000, lambda: splat_label.place_forget())  # Hide after 1 second

        threading.Thread(target=move_tomato, daemon=True).start()
    
    def check_hit(self, x, y):
        target_x, target_y = self.target_label.winfo_x(), self.target_label.winfo_y()
        if target_x - 50 < x < target_x + 200 and target_y - 50 < y < target_y + 200:
            messagebox.showinfo("Osuma!", "Tomaatti osui maalitauluun!")

    def reset_scores(self):
        # Tähän lisätään pisteiden nollauslogiikka
        pass

    

if __name__ == "__main__":
    root = tk.Tk()
    game = TomatoThrowGame(root)
    root.mainloop()

