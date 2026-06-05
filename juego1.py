import tkinter as tk
import random

W, H = 500, 500
CELL = 20
COLS = W // CELL
ROWS = H // CELL
FPS  = 120  # ms entre frames

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

canvas = tk.Canvas(root, width=W, height=H, bg="#1a1a2e", highlightthickness=0)
canvas.pack()

g = {
    "state":     "idle",
    "snake":     [(10, 10), (9, 10), (8, 10)],
    "direction": (1, 0),
    "next_dir":  (1, 0),
    "food":      (15, 10),
    "score":     0,
    "best":      0,
    "speed":     120,
    "after_id":  None,
}


def place_food():
    while True:
        pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if pos not in g["snake"]:
            g["food"] = pos
            return


def reset():
    g["snake"]     = [(10, 10), (9, 10), (8, 10)]
    g["direction"] = (1, 0)
    g["next_dir"]  = (1, 0)
    g["score"]     = 0
    g["speed"]     = 120
    place_food()


def draw():
    canvas.delete("all")

    # fondo con cuadricula sutil
    for r in range(ROWS):
        for c in range(COLS):
            x1, y1 = c*CELL, r*CELL
            shade = "#1c1c30" if (r+c) % 2 == 0 else "#1a1a2e"
            canvas.create_rectangle(x1, y1, x1+CELL, y1+CELL, fill=shade, outline="")

    # comida con efecto brillo
    fx, fy = g["food"]
    fx1, fy1 = fx*CELL+2, fy*CELL+2
    fx2, fy2 = fx1+CELL-4, fy1+CELL-4
    canvas.create_oval(fx1-2, fy1-2, fx2+2, fy2+2, fill="#ff4466", outline="")
    canvas.create_oval(fx1,   fy1,   fx2,   fy2,   fill="#ff6688", outline="")
    canvas.create_oval(fx1+4, fy1+2, fx1+8, fy1+6, fill="#ffaabb", outline="")

    # serpiente
    for i, (sx, sy) in enumerate(g["snake"]):
        x1, y1 = sx*CELL+1, sy*CELL+1
        x2, y2 = x1+CELL-2, y1+CELL-2
        t = i / max(len(g["snake"])-1, 1)
        # gradiente verde -> azul verdoso
        r_val = int(0   + (0   - 0)   * t)
        g_val = int(230 + (150 - 230) * t)
        b_val = int(100 + (200 - 100) * t)
        color = f"#{r_val:02x}{g_val:02x}{b_val:02x}"
        radius = 4 if i == 0 else 3
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", )
        # cabeza: ojos
        if i == 0:
            dx, dy = g["direction"]
            if dx == 1:   ex1,ey1,ex2,ey2 = x2-5,y1+3,x2-2,y1+7;  ex3,ey3,ex4,ey4 = x2-5,y2-7,x2-2,y2-3
            elif dx == -1: ex1,ey1,ex2,ey2 = x1+2,y1+3,x1+5,y1+7; ex3,ey3,ex4,ey4 = x1+2,y2-7,x1+5,y2-3
            elif dy == -1: ex1,ey1,ex2,ey2 = x1+3,y1+2,x1+7,y1+5; ex3,ey3,ex4,ey4 = x2-7,y1+2,x2-3,y1+5
            else:          ex1,ey1,ex2,ey2 = x1+3,y2-5,x1+7,y2-2; ex3,ey3,ex4,ey4 = x2-7,y2-5,x2-3,y2-2
            canvas.create_oval(ex1,ey1,ex2,ey2, fill="white", outline="")
            canvas.create_oval(ex3,ey3,ex4,ey4, fill="white", outline="")

    # HUD: puntuacion
    canvas.create_text(8, 8, anchor="nw",
                       text=f"puntos: {g['score']}",
                       font=("Courier",13,"bold"), fill="#00e5cc")
    canvas.create_text(W-8, 8, anchor="ne",
                       text=f"mejor: {g['best']}",
                       font=("Courier",13,"bold"), fill="#aaaacc")

    # pantalla idle / game over
    if g["state"] in ("idle", "dead"):
        canvas.create_rectangle(0, 0, W, H, fill="#000000", stipple="gray50")
        bx, by, bw, bh = W//2-130, H//2-90, 260, 180
        canvas.create_rectangle(bx, by, bx+bw, by+bh, fill="#0f0f23", outline="#00e5cc", width=2)
        if g["state"] == "idle":
            canvas.create_text(W//2, by+45, text="SNAKE",
                               font=("Courier",34,"bold"), fill="#00e5cc")
            canvas.create_text(W//2, by+90, text="Flechas para mover",
                               font=("Courier",13), fill="#aaaacc")
            canvas.create_text(W//2, by+115, text="Espacio para empezar",
                               font=("Courier",13), fill="#aaaacc")
        else:
            canvas.create_text(W//2, by+38, text="GAME OVER",
                               font=("Courier",26,"bold"), fill="#ff4466")
            canvas.create_text(W//2, by+80,
                               text=f"puntos: {g['score']}   mejor: {g['best']}",
                               font=("Courier",14,"bold"), fill="#ffffff")
            canvas.create_text(W//2, by+115, text="Espacio para reintentar",
                               font=("Courier",12), fill="#aaaacc")


def game_loop():
    if g["state"] == "playing":
        g["direction"] = g["next_dir"]
        hx, hy = g["snake"][0]
        dx, dy = g["direction"]
        nx, ny = hx+dx, hy+dy

        # colision pared
        if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
            g["state"] = "dead"
            if g["score"] > g["best"]:
                g["best"] = g["score"]
            draw()
            return

        # colision consigo mismo
        if (nx, ny) in g["snake"]:
            g["state"] = "dead"
            if g["score"] > g["best"]:
                g["best"] = g["score"]
            draw()
            return

        g["snake"].insert(0, (nx, ny))

        if (nx, ny) == g["food"]:
            g["score"] += 10
            # acelerar cada 5 comidas
            if g["score"] % 50 == 0 and g["speed"] > 60:
                g["speed"] = max(60, g["speed"] - 10)
            place_food()
        else:
            g["snake"].pop()

    draw()
    root.after(g["speed"], game_loop)


def key(event):
    k = event.keysym
    dx, dy = g["direction"]

    if g["state"] in ("idle", "dead"):
        if k == "space":
            reset()
            g["state"] = "playing"
            game_loop()
        return

    if k == "Right" and dx != -1: g["next_dir"] = (1,  0)
    elif k == "Left"  and dx !=  1: g["next_dir"] = (-1, 0)
    elif k == "Up"    and dy !=  1: g["next_dir"] = (0, -1)
    elif k == "Down"  and dy != -1: g["next_dir"] = (0,  1)


root.bind("<Key>", key)
root.focus_force()

draw()
root.mainloop()