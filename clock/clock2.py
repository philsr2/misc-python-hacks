"""
Shows a dial spinning once per second as an example of a simple animation.

Note: this demo is a GPL licensed example from tkinter_gl
It is modified to display 3 hands using time.localtime() and given adjustments 
to make the movement smoother by chatgpt.
"""

import tkinter
from tkinter import ttk
from tkinter_gl import GLCanvas
import time
import sys

try:
    from OpenGL import GL
except ImportError:
    raise ImportError(
        """
        This example requires PyOpenGL.

        You can install it with "pip install PyOpenGL".
        """)

class ClockWidget(GLCanvas):
    profile = 'legacy'

    dial_length = 0.9
    dial_counterlength = 0.1
    dial_width = 0.005

    min_length = 0.7
    min_counterlength = 0.1
    min_width =0.015

    hr_length = 0.5
    hr_counterlength = 0.1
    hr_width =0.03
    
    def __init__(self, parent):
        super().__init__(parent)

        self.start_time = time.time()

        self.is_first_draw = True

    def draw(self):
        self.make_current()
 
        GL.glViewport(0, 0, self.winfo_width(), self.winfo_height())

        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        
        t=time.localtime()

        GL.glPushMatrix()
        angle = -360.0 * t.tm_sec/60
        GL.glRotatef(angle, 0, 0, 1)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2d(  self.dial_width,  self.dial_length)
        GL.glVertex2d(  self.dial_width, -self.dial_counterlength)
        GL.glVertex2d( -self.dial_width, -self.dial_counterlength)
        GL.glVertex2d( -self.dial_width,  self.dial_length)
        GL.glEnd()
        GL.glPopMatrix()

        GL.glPushMatrix()
        min_angle = -360.0 * (t.tm_min+t.tm_sec/60)/60
        GL.glRotatef(min_angle, 0, 0, 1)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2d(  self.min_width,  self.min_length)
        GL.glVertex2d(  self.min_width, -self.min_counterlength)
        GL.glVertex2d( -self.min_width, -self.min_counterlength)
        GL.glVertex2d( -self.min_width,  self.min_length)
        GL.glEnd()
        GL.glPopMatrix()

        GL.glPushMatrix()
        hr_angle = -360.0 * (t.tm_hour % 12) / 12 - 0.5 * t.tm_min - (0.5 / 60) * t.tm_sec
        GL.glRotatef(hr_angle, 0, 0, 1)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2d(  self.hr_width,  self.hr_length)
        GL.glVertex2d(  self.hr_width, -self.hr_counterlength)
        GL.glVertex2d( -self.hr_width, -self.hr_counterlength)
        GL.glVertex2d( -self.hr_width,  self.hr_length)
        GL.glEnd()
        GL.glPopMatrix()

        while True:
            err = GL.glGetError()
            if err == GL.GL_NO_ERROR:
                break
            print("Error: ", err)

        self.swap_buffers()

        if self.is_first_draw:
            self.is_first_draw = False
            self.after(16, self.animate)

    def animate(self):
        self.draw()

        # We schedule a redraw almost immediately.
        #
        # Specifying a delay of 0 can cause a non-responsive
        # application on some operating systems.
        self.after(5, self.animate)

if __name__ == '__main__':
    root = tkinter.Tk()
    widget = ClockWidget(root)
    print("Using OpenGL", widget.gl_version())
    widget.pack(expand=True, fill='both', padx=50, pady=50)
    root.mainloop()
