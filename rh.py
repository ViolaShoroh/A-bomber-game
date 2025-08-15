import tkinter as tk
import random
from tkinter import messagebox

class Game(tk.Tk):
    def __init__(self, root):
        self.root = root
        main_menu = tk.Menu()
        main_menu.add_cascade(label="Об Авторе", command=self.show_about_window)
        root.config(menu=main_menu)
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()
        self.sky = self.canvas.create_rectangle(0, 0, 800, 500,
                                                fill='midnight blue',
                                                outline="midnight blue")
        self.eart = self.canvas.create_rectangle(0, 500, 800, 800,
                                                fill='black',
                                                outline="black")
        
        self.airplane_image = tk.PhotoImage(file="plane.png")
        self.airplane_image = self.airplane_image.subsample(2, 2)
        self.airplane = self.canvas.create_image(5, 5, anchor=tk.NW,
                                                 image=self.airplane_image)
        
        self.tank_image = tk.PhotoImage(file="tank.png")
        self.tank_image = self.tank_image.subsample(9, 9)
        self.tank = self.canvas.create_image(750, 500, anchor=tk.NW,
                                             image=self.tank_image)

        self.bomb = None  # Инициализация переменной для бомбы
        self.airplane_speed = random.randint(1, 3)  # Генерация случайной скорости самолета
        self.tank_speed = random.randint(1, 3)  # Генерация случайной скорости танка
        self.clouds = []
        for i in range(3):
            x = 100 + i * 300  # изменяем координаты по горизонтали
            y = 200
            size = 100
            cloud_parts = self.draw_cloud(x, y, size)
            self.clouds.append(cloud_parts)
        
        self.game_run()
        
    def show_about_window(self):
        window = tk.Toplevel()
        window.geometry("250x50")
        window.resizable(False, False)
        window.title("Об Авторе")
        lb1 = tk.Label(window, text="Работа выполнена студентом 2 курса")
        lb2 = tk.Label(window, text="Шморгай Виолой")
        lb1.pack(anchor='c')
        lb2.pack()
      
    def game_run(self):
        self.move_airplane()  # Движение самолета
        self.move_tank()  # Движение танка
        self.move_bomb()  # Движение бомбы
        self.root.after(20, self.game_run)  # Рекурсивный вызов game_run каждые 20 миллисекунд

    def draw_cloud(self, x, y, size):
        cloud_parts = []
        cloud_parts.append(self.canvas.create_oval(x - size // 2, y - size // 4,
                                                   x + size // 1.5, y + size // 4,
                                                   fill='gray64', outline='gray64'))
        cloud_parts.append(self.canvas.create_oval(x - size // 4, y - size // 3,
                                                   x + size // 4, y + size // 3,
                                                   fill='gray64', outline='gray64'))
        cloud_parts.append(self.canvas.create_oval(x + size // 4, y - size // 4,
                                                   x + size * 3 // 4, y + size // 4,
                                                   fill='gray64', outline='gray64'))
        return cloud_parts
 

    def drop_bomb(self, event):
        if self.bomb is None:
            airplane_coords = self.canvas.coords(self.airplane)
            x = airplane_coords[0]
            y = airplane_coords[1]
            self.bomb_image = tk.PhotoImage(file="Screenshot_7.png")
            self.bomb_image = self.bomb_image.subsample(15, 15)
            self.bomb = self.canvas.create_image(x, y,
                                             image=self.bomb_image)# Создание бомбы при нажатии пробела

    def move_bomb(self):
        if self.bomb is not None:
            self.canvas.move(self.bomb, 0, 30)
            bomb_coords = self.canvas.coords(self.bomb)
            tank_coords = self.canvas.coords(self.tank)
            overlapping = self.canvas.find_overlapping(*self.canvas.bbox(self.bomb))
            if self.tank in overlapping:
                self.canvas.delete(self.tank)
                self.canvas.delete(self.bomb)
                self.tank = self.canvas.create_image(750, 500, anchor=tk.NW,
                                             image=self.tank_image)
                messagebox.showinfo("Поздравляю!", "Противник уничтожен!")
                self.bomb = None
            elif self.canvas.coords(self.bomb)[1] >= 600:
                self.canvas.delete(self.bomb)
                self.bomb = None
                
    def move_airplane(self):
        airplane_x, airplane_y = self.canvas.coords(self.airplane)
        new_x = airplane_x + self.airplane_speed
        if new_x > self.canvas.winfo_width():
            new_x = 0
        self.canvas.coords(self.airplane, new_x, airplane_y)
        
    def move_tank(self):
        tank_x, tank_y = self.canvas.coords(self.tank)
        new_x = tank_x - self.tank_speed
        if new_x < -self.tank_image.width():
            new_x = self.canvas.winfo_width()
        self.canvas.coords(self.tank, new_x, tank_y)
        
if __name__ == '__main__':
    root = tk.Tk()  # Создание окна Tkinter
    root.geometry("800x600")
    root.resizable(False, False)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='6654739.png'))
    game = Game(root)  # Создание экземпляра игры
    root.bind("<space>", game.drop_bomb)  # Привязка функции к нажатию пробела
    root.title("Бомбардировщик")
    root.mainloop() # Запускаем главного цикла окна
