import tkinter as tk
from tkinter import Canvas, Button, Frame
from PIL import Image, ImageTk
import random
import threading
import pygame
import time

class TomatoThrowGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tomato Throwing Game")
        canvas = Canvas(root, width=1200, height=700)
        canvas.pack()

        # Pisteiden laskenta
        self.ernesti_score = 0
        self.kernesti_score = 0

        # Kuvat
        self.kernesti_img = self.load_image("kerne.png", (200, 200))
        self.ernesti_img = self.load_image("erne.png", (200, 200))
        self.maalitaulu_img = self.load_image("maalitaulu.png", (400, 400))
        self.tomaatti_img = self.load_image("tomaatti.png", (90, 70))
        self.tosuma_img = self.load_image("tosuma.png", (150, 150))

        # UI:n rakentaminen
        self.build_ui()

        # Äänet
        pygame.mixer.init()
        self.throw_sound = pygame.mixer.Sound("heitto.mp3")
        self.hit_sound = pygame.mixer.Sound("osuma.mp3")
        self.end_sound = pygame.mixer.Sound("loppu.mp3")
        self.missed_sound = pygame.mixer.Sound("ohitus.mp3")

    def play_sound(sound):
        sound.play()

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
        kernesti_x = 0
        kernesti_y = random.randint(0, 500)
        self.kernesti_label.place(x=kernesti_x, y=kernesti_y)

        # Maalitaulu keskelle
        self.target_label = tk.Label(self.root, image=self.maalitaulu_img)
        maalitaulu_x = 400-100
        maalitaulu_y = 300-100
        self.target_label.place(x=maalitaulu_x, y=maalitaulu_y)

        # Tulokset
        self.score_display = tk.Label(self.root, text="Pisteet: Kernesti: 0 | Ernesti: 0")
        self.score_display.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        # Painikkeet
        button_frame = Frame(root)
        button_frame.pack(pady=10)

        self.throw_kernesti = tk.Button(button_frame, text="Kernesti heittää", command=lambda: self.kernesti_throw_tomato())
        self.throw_kernesti.pack(side=tk.LEFT, padx=5)

        self.throw_ernesti = tk.Button(button_frame, text="Ernesti heittää", command=lambda: self.ernesti_throw_tomato())
        self.throw_ernesti.pack(side=tk.LEFT, padx=5)

        # Ernesti oikealle reunalle
        self.ernesti_move_btn = tk.Button(button_frame, text="Siirrä Ernesti", command=self.move_ernesti)
        self.ernesti_move_btn.pack(side=tk.LEFT, padx=5)
        self.ernesti_label = tk.Label(self.root, image=self.ernesti_img)
        ernesti_x = 800-100
        ernesti_y = random.randint(0, 500)
        self.ernesti_label.place(x=ernesti_x, y=ernesti_y)

        self.reset_button = Button(button_frame, text="Nollaa tulokset", command=self.reset_scores)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def move_ernesti(self):
        self.ernesti_label.place(x=700, y=random.randint(0, 500))

    def kernesti_throw_tomato(self):
        tx = 0
        ty = self.kernesti_label.winfo_y() + self.kernesti_img.height() // 2
        direction = 1
    
        tomato = tk.Label(self.root, image=self.tomaatti_img)
        tomato.place(x=tx, y=ty)

        self.throw_sound.play()

        dy = random.randint(-2000,2000)/500.0

        winthrow = self.kernesti_score - self.ernesti_score >= 2

        def move_tomato():
            nonlocal tx
            nonlocal ty

            limit = 400
            if winthrow:
                limit = 700

            if tx != limit:  # Move towards the target
                tx = tx + 5 * direction
                ty = ty + dy
                tomato.place(x=tx, y=ty)
                if tx != limit:
                    self.root.after(20, move_tomato)
                else:
                    tomato.destroy()
                    self.hit_sound.play()
                    target_hit = self.check_hit(tx, ty + 35, winthrow)
                    if target_hit:
                        if winthrow:
                            pass
                        else:
                            self.kernesti_score += 1
                            self.update_scores()
                            threading.Thread(target=self.show_splat, daemon=True).start()
                    else:
                        self.missed_sound.play()
                        threading.Thread(target=self.show_failure, daemon=True).start()

        threading.Thread(target=move_tomato, daemon=True).start()

    def ernesti_throw_tomato(self):
        tx = 700
        ty = self.ernesti_label.winfo_y() + self.ernesti_img.height() // 2
        direction = -1
    
        tomato = tk.Label(self.root, image=self.tomaatti_img)
        tomato.place(x=tx, y=ty)

        self.throw_sound.play()
        dy = random.randint(-2000,2000)/500.0
        def move_tomato():
            nonlocal tx
            nonlocal ty
            if tx != 400:  # Move towards the target
                tx = tx + 5 * direction
                ty = ty + dy  # start_y - (400 - tx) * 0.2  # This creates the arc
                tomato.place(x=tx, y=ty)
                if tx != 400:
                    self.root.after(20, move_tomato)
                else:
                    tomato.destroy()
                    self.hit_sound.play()
                    target_hit = self.check_hit(tx, ty + 35)
                    if target_hit:
                        self.ernesti_score += 1
                        self.update_scores()
                        threading.Thread(target=self.show_splat, daemon=True).start()
                    else:
                        self.missed_sound.play()
                        threading.Thread(target=self.show_failure, daemon=True).start()                    
                
        threading.Thread(target=move_tomato, daemon=True).start()
    
    def show_splat(self):
        splat_label = tk.Label(self.root, image=self.tosuma_img)
        splat_label.place(x=400, y=300)
        time.sleep(1)
        splat_label.destroy()

    def show_failure(self):
        failure_label = tk.Label(self.root, text="Ohi meni!", fg="red", font=("Helvetica", 16))
        failure_label.place(x=400, y=300)
        time.sleep(1)
        failure_label.destroy()

    def check_hit(self, y):
        target_hit = y > 320 and y < 395
        return target_hit

    def reset_scores(self):
        self.ernesti_score = 0
        self.kernesti_score = 0
        self.update_scores()
    
    def update_scores(self):
        self.score_display.config(text=f"Pisteet: Kernesti: {self.kernesti_score} | Ernesti: {self.ernesti_score} ")

if __name__ == "__main__":
    root = tk.Tk()
    game = TomatoThrowGame(root)
    root.mainloop()

