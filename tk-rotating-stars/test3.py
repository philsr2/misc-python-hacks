
import numpy as np
import tkinter as tk
import random

random.seed(7)

# --- 100 random star systems ---
# X = left/right,  Z = up/down,  Y = depth (camera is out at Y+)
N = 1000
pts = np.array([
    [random.uniform(-18, 18),   # X
     random.uniform(-18, 18),   # Y
     random.uniform(-18, 18)]   # Z
    for _ in range(N)
], dtype=float)

W, H   = 1600, 960
angle  = 0.0
SENS   = 0.4
drag_x = None

# camera sits at Y = +CAM_D looking toward origin
CAM_D  = 8.0
FOCAL  = 300.0     # perspective strength


def rotate_z(points, angle_deg):
    """Rotate around Z (up/down) â€” swings stars left/right."""
    a = np.radians(angle_deg)
    R = np.array([
        [ np.cos(a), -np.sin(a), 0],
        [ np.sin(a),  np.cos(a), 0],
        [         0,          0, 1],
    ])
    return points @ R.T


def project(points):
    """
    Camera is at Y = +CAM_D looking toward -Y.
    depth  = CAM_D - Y   (positive means in front of camera)
    screen_x =  X / depth * FOCAL
    screen_y = -Z / depth * FOCAL   (flip so Z+ is up on screen)
    """
    depth  = CAM_D - points[:, 1]
    depth  = np.where(depth < 0.1, 0.1, depth)   # don't divide by ~zero

    sx =  points[:, 0] / depth * FOCAL + W / 2
    sy = -points[:, 2] / depth * FOCAL + H / 2
    return sx, sy, depth


def draw():
    canvas.delete('all')

    rotated        = rotate_z(pts, angle)
    sx, sy, depth  = project(rotated)

    # radius: largest when depth is smallest (closest)
    d_min, d_max = depth.min(), depth.max()
    R_NEAR, R_FAR = 4,1 

    # sort back-to-front so near stars draw on top
    order = np.argsort(depth)[::-1]

    for i in order:
        t = (depth[i] - d_min) / (d_max - d_min + 1e-6)  # 0=near, 1=far
        r = R_NEAR + t * (R_FAR - R_NEAR)

        # colour: near = bright warm white, far = dim blue-grey
        bright = int(255 - t * 160)
        blue   = int(180 - t * 80)
        color  = f'#{bright:02x}{bright:02x}{blue:02x}'

        x, y = sx[i], sy[i]
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           fill=color, outline='', )

    canvas.create_text(10, 10, anchor='nw', fill='#556',
                       text=f'Z-rotation: {angle % 360:.1f}Â°  |  right-drag to rotate')


def on_press(event):
    global drag_x
    drag_x = event.x

def on_drag(event):
    global angle, drag_x
    if drag_x is not None:
        angle  += (event.x - drag_x) * SENS
        drag_x  = event.x
        draw()

def on_release(event):
    global drag_x
    drag_x = None


root = tk.Tk()
root.title('Star Sector  |  camera at Y+  |  right-drag to rotate')
canvas = tk.Canvas(root, width=W, height=H, bg='#03030a')
canvas.pack()

canvas.bind('<Button-3>',        on_press)
canvas.bind('<B3-Motion>',       on_drag)
canvas.bind('<ButtonRelease-3>', on_release)

draw()
root.mainloop()
