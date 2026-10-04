import tkinter as tk
import random

# ตั้งค่าพื้นฐาน
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20
SPEED = 100  # ความเร็วของเกม (มิลลิวินาที)

# สร้างหน้าจอ
root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)

# สร้างพื้นหลัง
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# สร้างตัวเกม
snake = [(WIDTH//2, HEIGHT//2)]
direction = "Right"
food = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, 
        random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)

def draw():
    canvas.delete("all")
    # วาดอาหาร
    canvas.create_rectangle(food[0], food[1], food[0]+BLOCK_SIZE, food[1]+BLOCK_SIZE, fill="red")
    # วาดงู
    for x, y in snake:
        canvas.create_rectangle(x, y, x+BLOCK_SIZE, y+BLOCK_SIZE, fill="lime")
    root.after(SPEED, move)

def move():
    global food

    head = snake[0]
    x, y = head

    if direction == "Right":
        new_head = (x + BLOCK_SIZE, y)
    elif direction == "Left":
        new_head = (x - BLOCK_SIZE, y)
    elif direction == "Up":
        new_head = (x, y - BLOCK_SIZE)
    elif direction == "Down":
        new_head = (x, y + BLOCK_SIZE)

    # ตรวจสอบการชนขอบหรือตัวเอง
    if (new_head in snake or 
        new_head[0] < 0 or new_head[0] >= WIDTH or 
        new_head[1] < 0 or new_head[1] >= HEIGHT):
        return

    # ตรวจสอบการกินอาหาร
    if new_head == food:
        snake.insert(0, new_head)
        food = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, 
                random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)
    else:
        snake.pop()
        snake.insert(0, new_head)

    draw()

def change_direction(new_dir):
    global direction
    if new_dir == "Right" and direction != "Left":
        direction = new_dir
    elif new_dir == "Left" and direction != "Right":
        direction = new_dir
    elif new_dir == "Up" and direction != "Down":
        direction = new_dir
    elif new_dir == "Down" and direction != "Up":
        direction = new_dir

# สร้างปุ่มควบคุม
start_button = tk.Button(root, text="เริ่มเกม", command=lambda: start_game())
start_button.pack()

def start_game():
    global direction, snake, food
    direction = "Right"
    snake = [(WIDTH//2, HEIGHT//2)]
    food = (random.randint(0, (WIDTH//BLOCK_SIZE)-1) * BLOCK_SIZE, 
            random.randint(0, (HEIGHT//BLOCK_SIZE)-1) * BLOCK_SIZE)
    draw()

# จัดการการกดคีย์
def key_press(event):
    if event.keysym == "Right":
        change_direction("Right")
    elif event.keysym == "Left":
        change_direction("Left")
    elif event.keysym == "Up":
        change_direction("Up")
    elif event.keysym == "Down":
        change_direction("Down")

root.bind("<KeyPress>", key_press)

# เริ่มเกม
start_game()
root.mainloop()