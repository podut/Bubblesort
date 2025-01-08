import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithms Visualizer")
        self.num_elements = 50  # numărul inițial de elemente
        self.speed = 0.1  # viteza animației
        self.array = []
        self.is_sorting = False  # Flag pentru a verifica dacă sortarea este în curs
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        # Creăm un slider pentru a schimba numărul de elemente
        self.num_elements_slider = tk.Scale(root, from_=5, to_=100, orient="horizontal", label="Numărul de elemente")
        self.num_elements_slider.set(self.num_elements)
        self.num_elements_slider.pack()

        # Creăm un slider pentru a schimba viteza animației
        self.speed_slider = tk.Scale(root, from_=0.01, to_=0.5, orient="horizontal", label="Viteza animației", resolution=0.01)
        self.speed_slider.set(self.speed)
        self.speed_slider.pack()

        # Creăm o etichetă care va afișa valoarea curentă a vitezei
        self.speed_label = tk.Label(root, text=f"Viteza: {self.speed}")
        self.speed_label.pack()

        # Butoane pentru a începe și a opri sortarea
        self.start_button = tk.Button(root, text="Start Sortare", command=self.start_sorting)
        self.start_button.pack()

        self.reset_button = tk.Button(root, text="Resetare", command=self.reset_array)
        self.reset_button.pack()

        self.quit_button = tk.Button(root, text="Ieșire", command=root.quit)
        self.quit_button.pack()

        self.reset_array()

        # Actualizarea etichetei de viteză în timp real
        self.speed_slider.bind("<Motion>", self.update_speed_label)

    def reset_array(self):
        # Oprim sortarea în cazul în care este activă
        if self.is_sorting:
            self.is_sorting = False
        # Resetăm array-ul și actualizăm canvas-ul
        self.num_elements = self.num_elements_slider.get()
        self.speed = self.speed_slider.get()
        self.array = [random.randint(10, 300) for _ in range(self.num_elements)]
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        width = 600
        bar_width = width / len(self.array)
        for i, value in enumerate(self.array):
            self.canvas.create_rectangle(i * bar_width, 400 - value, (i + 1) * bar_width, 400, fill="blue")

    def update_speed_label(self, event):
        """Actualizează eticheta vitezei în timp real pe măsură ce slider-ul este ajustat."""
        self.speed = self.speed_slider.get()
        self.speed_label.config(text=f"Viteza: {self.speed}")

    def bubble_sort(self):
        arr = self.array[:]
        n = len(arr)
        for i in range(n):
            if not self.is_sorting:
                break  # Opriți sortarea dacă butonul de reset a fost apăsat
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    self.array = arr
                    self.update_canvas()
                    self.root.update_idletasks()  # Refresh the UI
                    self.speed = self.speed_slider.get()  # Actualizăm viteza în timpul sortării
                    time.sleep(self.speed)

        self.is_sorting = False  # Setăm flag-ul să fie fals când sortarea se încheie

    def start_sorting(self):
        if not self.is_sorting:
            self.is_sorting = True
            threading.Thread(target=self.bubble_sort).start()  # Rulăm sortarea într-un thread separat

if __name__ == "__main__":
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()
