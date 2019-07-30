#-*-coding:utf8;-*-
#qpy:3
#qpy:console
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import random
import math

class point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"


def antipodal(p,q,a):
    dx = abs(p.x - q.x)
    dy = abs(p.y - q.y)
    if(p.x >= q.x and p.y >= q.y):
        r = point(q.x - a*dx, q.y - a*dy)
        return r                
    elif(p.x <= q.x and p.y <= q.y):
        r = point(q.x + a*dx, q.y + a*dy)
        return r
    elif(p.x >= q.x and p.y <= q.y):
        r = point(q.x - a*dx, q.y + a*dy)
        return r                
    elif(p.x <= q.x and p.y >= q.y):
        r = point(q.x + a*dx, q.y - a*dy)
        return r                
    else:   
        print("it´s de same point")
        return p

def calc_angulo(a, b, c):
    #ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
    return ang + 360 if ang < 0 else ang

def calc_tangente(polygon, p):
    p0 = point(p.x+1, p.y)
    ang_i = None
    ang_min = 361
    ang_max = 0
    p_min = None
    p_max = None
    for pi in polygon:
        ang_i = calc_angulo(p0, p, pi)
        if(ang_min > ang_i):
            ang_min = ang_i
            p_min = pi
        
        if(ang_max < ang_i):
            ang_max = ang_i
            p_max = pi
    return (p_min, p_max)



def orbita(puntos, p, a):
    """
    puntos -> conjunto de puntos en orden a visitar
    p -> punto de inicio
    a -> factor de crecimiento
    """
    orbit = []
    pi = p
    for qi in puntos:
        pj = antipodal(pi, qi, a)
        print("p: "+str(pi)+" q: "+str(qi)+" antipodal: "+str(pj))
        orbit.append((pi, qi, pj))
        pi = pj

    return orbit

def cierre_convexo(puntos):
    puntos_np = np.array(puntos)
    ch = ConvexHull(puntos_np)
    return ch.simplices


def orbita_convexo(polygon, p, a):
    """
    polygon -> conjunto de puntos en orden a visitar
    p -> punto de inicio
    a -> factor de crecimiento
    """
    return



def dibuja(puntos):
    colors = (0,0,0)
    area = np.pi*3
    # Plot
    x = []
    y = []
    lineas = []
    x1 = []
    y1 = []
    ch = []
    for p in puntos:
        x1.append(p[1].x)
        x.append(p[2].x)
        y1.append(p[1].y)
        y.append(p[2].y)
        lineas.append([(p[0].x, p[0].y), (p[2].x, p[2].y)])
        ch.append([p[1].x, p[1].y])

    lc = mc.LineCollection(lineas, linewidths=1)
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    #ax.autoscale()
    ax.margins(0,1)
    #print(x)
    #print(y)

    puntos_np = np.array(ch)
    #puntos_np = np.random.rand(5,2)
    convexo = ConvexHull(puntos_np)
    for x in convexo:
        plt.plot(puntos_np[x, 0], puntos_np[x, 1], 'k-')


    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.scatter(x1, y1, s=area, c='red', alpha=0.5)
    plt.title('Orbit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


# Create data
ps = []
ps_lista = []
for x in range(5):
    p_new = point(random.randrange(20), random.randrange(20))
    ps.append(p_new)
    ps_lista.append([p_new.x, p_new.y])

#mi_orbita = orbita(ps, point(random.randrange(20), random.randrange(20)), 1)
#dibuja(mi_orbita)


print("tangentes")
print("-----------------------------------------------------------")
#print(type(cierre_convexo(ps_lista)))
#print(cierre_convexo(ps_lista))
mi_ch = cierre_convexo(ps_lista)
mi_ch_simplex = []
for simplex in mi_ch:
    print(simplex)
    mi_ch_simplex.append(point(simplex[0], simplex[1]))
    
angulos = calc_tangente(mi_ch_simplex, point(random.randrange(20), random.randrange(20)))
print(angulos[0])
print(angulos[1])

# print("------------------------------------------------------")
# print("sobre el ejex")
# p1 = point(1,0)
# p2 = point(3,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))
# p1 = point(3,0)
# p2 = point(1,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))
# print("------------------------------------------------------")
# print("cuadrante I")
# p1 = point(3,5)
# p2 = point(1,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))
# print("------------------------------------------------------")
# print("cuadrante II")
# p1 = point(-3,2)
# p2 = point(1,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))
# print("------------------------------------------------------")
# print("cuadrante III")
# p1 = point(-3,-3)
# p2 = point(1,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))
# print("------------------------------------------------------")
# print("cuadrante IV")
# p1 = point(3,-2)
# p2 = point(1,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))
# print("------------------------------------------------------")
# print("puntos iguales")
# p1 = point(1,0)
# p2 = point(1,0)
# print("p1: "+str(p1))
# print("p2: "+str(p2))
# print(antipodal(p1,p2,1))













