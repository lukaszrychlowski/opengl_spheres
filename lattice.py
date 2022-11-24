import numpy as np
import random
from glumpy import app, gl, glm, gloo

vertex = """
    uniform mat4 model; 
    uniform mat4 view; 
    uniform mat4 projection;
    uniform float antialias;
    attribute vec3 position;
    attribute float radius;
    varying float v_pointsize;
    varying float v_radius;

    void main(){
        v_radius = radius;
        gl_Position = projection * view * model * vec4(position,1.0); 
        gl_PointSize = 2.0 * (v_radius + 1.5*antialias);
    }"""


fragment = """
    uniform float antialias;
    varying float v_radius;

    void main()
    {
        float r = (v_radius + 2.0*antialias);
        float signed_distance = length(gl_PointCoord.xy - vec2(0.5,0.5)) * 2 * r - v_radius;
        if( signed_distance < 0 ){
            gl_FragColor = vec4(0.0, 0.0, 0.0, 0.8);
        } 
        else{
            discard;
        }
    }
"""

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

for ii in range(0,250,50):
    for i in range(N):
        lattice = np.vstack([lattice, random_point(ii)])

#print(lattice)
#print(lattice)
#np.savetxt("lattice1.csv", lattice, delimiter=";")

program = gloo.Program(vertex, fragment)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0.2, 0.3, -700)

program['position'] = lattice
#program['position'] = np.random.randn(1000,3)
program['radius']   = np.full(len(lattice), 1)
#program['radius'] = 2.0
program['antialias'] = 1.0
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
