import tkinter as tk
import random
import time
import threading

# Global variables
array = []
is_sorting = False
speed = 0.1
stop_sorting = False  # Flag pentru a opri sortarea

def reset_array():
    global array, is_sorting, stop_sorting
    if is_sorting:
        stop_sorting = True  # Oprim sortarea dacă este activă
    is_sorting = False  # Oprim sortarea
    stop_sorting = False  # Resetăm stop flag
    num_elements = num_elements_slider.get()
    array = [random.randint(10, 300) for _ in range(num_elements)]
    update_canvas()

def update_canvas():
    canvas.delete("all")
    width = 600
    bar_width = width / len(array)
    for i, value in enumerate(array):
        canvas.create_rectangle(i * bar_width, 400 - value, (i + 1) * bar_width, 400, fill="blue")

def update_speed_label(event):
    global speed
    speed = speed_slider.get()
    speed_label.config(text=f"Viteza: {speed}")

def bubble_sort():
    global array, is_sorting, stop_sorting
    arr = array[:]
    n = len(arr)
    for i in range(n):
        if stop_sorting:  # Verificăm dacă trebuie să oprim sortarea
            break
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                array = arr
                # Folosim root.after() pentru a actualiza UI-ul din main thread
                root.after(0, update_canvas)
                root.after(0, root.update_idletasks)  # Actualizează interfața
                time.sleep(speed)
    is_sorting = False  # Oprim sortarea
    stop_sorting = False  # Resetăm stop flag

def start_sorting():
    global is_sorting, stop_sorting
    if not is_sorting and not stop_sorting:
        is_sorting = True
        threading.Thread(target=bubble_sort, daemon=True).start()  # Rulăm sortarea într-un thread separat

def stop_sorting_func():
    global stop_sorting
    stop_sorting = True  # Setăm stop flag pentru a opri sortarea

root = tk.Tk()
root.title("Sorting Algorithms Visualizer")

# Slider pentru numărul de elemente
num_elements_slider = tk.Scale(root, from_=5, to_=100, orient="horizontal", label="Numărul de elemente")
num_elements_slider.set(50)
num_elements_slider.pack()

# Slider pentru viteza animației
speed_slider = tk.Scale(root, from_=0.01, to_=0.5, orient="horizontal", label="Viteza animației", resolution=0.01)
speed_slider.set(0.1)
speed_slider.pack()

# Etichetă pentru a arăta viteza curentă
speed_label = tk.Label(root, text="Viteza: 0.1")
speed_label.pack()

# Buton pentru a începe sortarea
start_button = tk.Button(root, text="Start Sortare", command=start_sorting)
start_button.pack()

# Buton pentru a reseta array-ul
reset_button = tk.Button(root, text="Resetare", command=reset_array)
reset_button.pack()

# Buton pentru a opri sortarea
stop_button = tk.Button(root, text="Stop Sortare", command=stop_sorting_func)
stop_button.pack()

# Buton pentru a ieși din aplicație
quit_button = tk.Button(root, text="Ieșire", command=root.quit)
quit_button.pack()

# Canvas pentru a vizualiza sortarea
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Inițializăm array-ul
reset_array()

# Actualizăm eticheta de viteză în timp real
speed_slider.bind("<Motion>", update_speed_label)

# Pornim loop-ul principal Tkinter
root.mainloop()
