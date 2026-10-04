# Snake Game Logic Evaluation Report

This report analyzes the core game logic of two Python Snake Game implementations: **Model 1 (GLM-4 9B)** and **Model 2 (Qwen 3 8B)**. Both models were independently instructed with the identical specification:

> **Benchmark Prompt:**  
> `"สร้างเกมงู (Snake Game) ด้วย Python พร้อมหน้าจอ GUI และปุ่มเริ่มเกม"`  
> *(English translation: "Create a Snake Game using Python with a GUI window and a game start button.")*

---

## Model 1 (GLM-4 9B)

1. **Body Movement Logic**
   The snake moves by updating its position using `x1_change` and `y1_change` values, then appending a new head position to the `snake_list`.

2. **Reverse Prevention**
   Yes, there is logic to prevent the snake from reversing into itself. Direction changes are checked against opposite directions before being allowed.

3. **Self-Collision Logic**
   The game checks if the snake's head is colliding with its own body by comparing the head's position to the positions in the `snake_list` (excluding the tail).

4. **Smart Food Spawning**
   Yes, the code ensures new food does not spawn on the snake's body. The check is performed when the snake eats food.

## Model 2 (QWEN)

1. **Body Movement Logic**
   The snake moves by calculating a new head position based on the current direction and then inserting the new head into the `snake` list.

2. **Reverse Prevention**
   Yes, there is logic to prevent the snake from reversing into itself. Direction changes are checked against opposite directions before being allowed.

3. **Self-Collision Logic**
   The game checks for self-collision by ensuring the new head position is not already in the `snake` list and that it is within the canvas boundaries.

4. **Smart Food Spawning**
   Yes, the code ensures new food does not spawn on the snake's body. The check is performed when the snake eats food.