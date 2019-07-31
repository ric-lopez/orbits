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

def lado_p_a_segmento(v1, v2, p):
        """Determina de que lado se encuentra el punto 'p' con respecto a la arista (v1, v2)"""
        #area = (v2.getX()-v1.getX())*(p.getY()- v1.getY())-(p.getX()-v1.getX())*(v2.getY()-v1.getY())
        area = (v2.x-v1.x)*(p.y- v1.y)-(p.x-v1.x)*(v2.y-v1.y)
        if (area > 0):
            lado = "izq"
        elif (area < 0):
            lado = "der"
        else:
            lado = "col"
        return lado


def calc_angulo(a, b, c):
    #ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
    return ang + 360 if ang < 0 else ang

def calc_tangente(polygon, p):
    #p0 = point(p.x+1, p.y)
    p0 = point(0,0)
    ang_i = None
    angulos = []

    for pi in polygon:
        angulos.append(calc_angulo(p0, p, pi))

    ang_min = min(angulos)
    ang_max = max(angulos)
    p_min = polygon[angulos.index(ang_min)]
    p_max = polygon[angulos.index(ang_max)]
    return (p_min, p_max)


# def calc_tangente(polygon, p):
#     p0 = point(p.x+1, p.y)
#     ang_i = None
#     ang_min = 361
#     ang_max = 0
#     p_min = None
#     p_max = None
#     for pi in polygon:
#         ang_i = calc_angulo(p0, p, pi)
#         if(ang_min > ang_i):
#             ang_min = ang_i
#             p_min = pi
        
#         if(ang_max < ang_i):
#             ang_max = ang_i
#             p_max = pi
#     return (p_min, p_max)


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
    v_lista = []
    for v in ch.vertices:
        print(ch.points[v])
        v_lista.append(point(ch.points[v][0],ch.points[v][1]))
    return v_lista


def orbita_convexo(polygon, p, a, direccion):
    """
    polygon -> conjunto de puntos en orden a visitar
    p -> punto de inicio
    a -> factor de crecimiento
    """
    tangentes = calc_tangente(polygon, p)
    vuelta1 = lado_p_a_segmento(tangentes[0], p, tangentes[1])
    vuelta2 = lado_p_a_segmento(tangentes[1], p, tangentes[0])
    if(vuelta1 == "der"):
        t_der = tangentes[1]
        t_izq = tangentes[0]
        print(vuelta1)
        print(t_der)
        print(vuelta2)
        print(t_izq)
    elif(vuelta1 == "izq"):
        t_izq = tangentes[1]
        t_der = tangentes[0]
        print(vuelta1)
        print(t_der)
        print(vuelta2)
        print(t_izq)
    #vuelta2 = lado_p_a_segmento(tangentes[1], p, tangentes[0])
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
#p_inicio = point(random.randrange(20), random.randrange(20))
p_inicio = point(25, 1)
print(p_inicio)
print("------------------------")
for aux in mi_ch:
    print(str(aux))
print("------------------------")    
angulos = calc_tangente(mi_ch, p_inicio)
print(angulos[0])
print(angulos[1])
print("-------------------------")
orbita_convexo(mi_ch, p_inicio, 1, "derecha")

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













