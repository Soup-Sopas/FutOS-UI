import tkinter as tk
import random

class PongFutOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong FutOS Deluxe")
        self.canvas = tk.Canvas(root, width=1000, height=600, bg="#1e1e1e")
        self.canvas.pack()

        self.paddle_speed = 25
        self.ball_speed = [6, 6]

        self.paddle1 = self.canvas.create_rectangle(50, 250, 70, 350, fill="#50fa7b", width=0)
        self.paddle2 = self.canvas.create_rectangle(930, 250, 950, 350, fill="#ff5555", width=0)

        self.ball = self.canvas.create_oval(490, 290, 510, 310, fill="#f1fa8c", width=0)

        self.score1 = 0
        self.score2 = 0
        self.score_text = self.canvas.create_text(500, 40, fill="white", font=("Courier New", 30, "bold"),
                                                  text="0     |     0")

        self.status_text = self.canvas.create_text(500, 70, fill="#8be9fd", font=("Courier New", 14),
                                                   text="Jugador 1     -     Jugador 2")

        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.move_paddles)
        self.canvas.bind("<Escape>", lambda event: self.root.destroy())

        self.update_ball()


    def move_paddles(self, event):
        if event.keysym == "w":
            self.canvas.move(self.paddle1, 0, -self.paddle_speed)
        elif event.keysym == "s":
            self.canvas.move(self.paddle1, 0, self.paddle_speed)
        elif event.keysym == "Up":
            self.canvas.move(self.paddle2, 0, -self.paddle_speed)
        elif event.keysym == "Down":
            self.canvas.move(self.paddle2, 0, self.paddle_speed)

    def update_ball(self):
        self.canvas.move(self.ball, *self.ball_speed)

        ball_coords = self.canvas.coords(self.ball)
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        # Rebote en arriba/abajo
        if ball_coords[1] <= 0 or ball_coords[3] >= 600:
            self.ball_speed[1] = -self.ball_speed[1]

        # Rebote en paletas
        if self.collides(ball_coords, paddle1_coords):
            self.ball_speed[0] = abs(self.ball_speed[0])
        elif self.collides(ball_coords, paddle2_coords):
            self.ball_speed[0] = -abs(self.ball_speed[0])

        # Punto jugador 2
        if ball_coords[0] <= 0:
            self.score2 += 1
            self.reset_ball(direction=1)
        # Punto jugador 1
        elif ball_coords[2] >= 1000:
            self.score1 += 1
            self.reset_ball(direction=-1)

        self.canvas.itemconfig(self.score_text, text=f"{self.score1}     |     {self.score2}")
        self.root.after(30, self.update_ball)

    def reset_ball(self, direction):
        self.canvas.coords(self.ball, 490, 290, 510, 310)
        self.ball_speed = [6 * direction, random.choice([-6, 6])]

    def collides(self, ball, paddle):
        return not (ball[2] < paddle[0] or ball[0] > paddle[2] or
                    ball[3] < paddle[1] or ball[1] > paddle[3])

