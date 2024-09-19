# OpenGL-Engine
A basic OpenGL-based application engine based on a tutorial from the YouTube channel Coder Space.

Original Tutorial: "Let's code 3D Engine in Python. OpenGL Pygame Tutorial" by Coder Space.
https://www.youtube.com/watch?v=eJDIsFJN4OQ&list=PLddGrbqhjeY5os8FyOPhGNJLsnJ08oTfh&index=4

Requirements:
Requires Python 3.10 and the following dependencies to be installed via pip:
  1) PyGLM
  2) PyOpenGL
  3) modernGL
  4) numpy
  5) pygame

Running the application:
  1) Download the repository from the "master" branch
  2) Run "main.py" using Python from the command line

The application runs a window which tests several features:
  1) Loading a texture from a file
  2) Rendering that texture to the screen with a custom scale and x-y coordinate
  3) Handling interrupt events, including:
      a) Reacting to a keyboard event
      b) Detecting mouse movement and determining possible collisions within a border (a "hover" event)
      c) Reacting to a mouse click
      d) Reacting to window close events
  5) Dynamically changing an object's texture
  6) Dynamically changing an object's position
  7) Dynamically changing an object's rotation
      a) When an object's rotation changes, it's rectangular collision box will also rotate with it
  8) Playing an "animation" which can change an object's position or rotation based on a time-dependent function (e.g., acceleration)


Testing window controls:
The top-left rectangle:
  1) Hovering over the rectangle begins a rotation animation. The rotation rate is dependent on the amount of time that the mouse hovers over the rectangle. The angular velocity will begin at zero and increase over time, approaching a limit.
  2) Hovering over the rectangle will also change the rectangle's texture to a wooden crate. Note that the bounds for mouse-collision detection rotate with the rectangle.
  3) Holding left-clicking over the rectangle will change the rectangle's texture to an iron crate. Letting go of left-click will revert the texture to the wooden texture.
  4) Right-clicking the rectangle will change the rectangle's texture to a brass crate. Letting go of right-click will revert the texture to the wooden texture.
  5) If the mouse colliding with the rectangle, no matter the current state of the object, the rectangle will cease rotating (but keep its current rotation) and revert back to the test texture.

The bottom-center rectangle:
  1) Holding w, a, s, or d will move the rectangle up, left, down, or right respectively.
  2) Holding multiple movement keys simultaneously will sum their effects. E.g., holding w and a will move the rectangle up and left, while holding a and s will halt movement.
  3) Pressing v will cycle the rectangle's texture upon key release.

