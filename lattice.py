import numpy as np
import random
from glumpy import app, gl, glm, gloo

vertex = """
    uniform mat4 model; 
    uniform mat4 view; 
    uniform mat4 projection;
    attribute vec3 position;
    void main(){
        gl_Position = projection * view * model * vec4(position,1.0); 
        gl_PointSize = 2.0;
    }"""

fragment = """
    void main(){
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }"""

window = app.Window(color=(1,1,1,0))

theta, phi = 0, 0
m = 5  
n = (2*m)**3
lattice = np.zeros((n,3), dtype=np.float32)
#dx, dy, dz = 0, 0, 0

i=0
for x in range(-m,m,1):
    for y in range(-m,m,1):
        for z in range(-m,m,1):
            dx = random.uniform(-.03, .03)
            dy = random.uniform(-.03, .03)
            dz = random.uniform(-.03, .03)
            lattice[i]=[x+dx,y+dy,z+dz]
            i += 1

lattice = lattice*0.3

#print(lattice)
#np.savetxt("lattice1.csv", lattice, delimiter=";")

program = gloo.Program(vertex, fragment)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0.2, 0.3, -10)


program['position'] = lattice
program['model'] = np.eye(4, dtype=np.float32)
program['projection'] = np.eye(4, dtype=np.float32)
program['view'] = view

@window.event
def on_draw(dt):
    global theta, phi
    window.clear()
    program.draw(gl.GL_POINTS)
    theta += .02
    phi += .02
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    program['model'] = model 

@window.event
def on_resize(width, height):
    program['projection'] = glm.perspective(45.0, width / float(height), 1.0, 1000.0)


gl.glEnable(gl.GL_DEPTH_TEST)
app.run()
