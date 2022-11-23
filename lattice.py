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


def normalize(vec):
    vec = vec * (1 / np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2))
    #print(np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2))
    return vec

def random_point(sphere_radius): ## normalized
    vec = np.array([np.random.normal(0, scale=1.0),
                    np.random.normal(0, scale=1.0),
                    np.random.normal(0, scale=1.0)])
    return normalize(vec) * sphere_radius

M = 10
N = 10000

lattice = np.zeros(3)

for ii in range(10,250,50):
    for i in range(N):
        lattice = np.append(lattice, random_point(ii))

#print(lattice)
#print(lattice)
#np.savetxt("lattice1.csv", lattice, delimiter=";")

program = gloo.Program(vertex, fragment)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0.2, 0.3, -700)


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
