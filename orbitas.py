#-*-coding:utf8;-*-
#qpy:3
#qpy:console
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import random
import math
import sys

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
    
    if(direccion == "derecha"):
        orbit = []
        pi = p
        qi = t_der
        for i in range(5):
            pj = antipodal(pi, qi, a)
            print("p: "+str(pi)+" q: "+str(qi)+" antipodal: "+str(pj))
            orbit.append((pi, qi, pj))
            tangentes = calc_tangente(polygon, pj)
            pi = pj
            if(qi == tangentes[0]):
                qi = tangentes[1]
            else:
                qi = tangentes[0]

    return orbit



def dibuja(orbita):
    colors = (0,0,0)
    area = np.pi*3
    # Plot
    x = []
    y = []
    lineas = []
    x1 = []
    y1 = []
    #ch = []
    for p in orbita:
        x1.append(p[1].x)
        x.append(p[2].x)
        y1.append(p[1].y)
        y.append(p[2].y)
        lineas.append([(p[0].x, p[0].y), (p[2].x, p[2].y)])
        #ch.append([p[1].x, p[1].y])

    lc = mc.LineCollection(lineas, linewidths=1)
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.margins(0,1)

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.scatter(x1, y1, s=area, c='red', alpha=0.5)
    plt.title('Orbit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def dibuja_convexo(polygon, orbita):

    # plot
    colors = (0,0,0)
    area = np.pi*3
    x = []
    y = []
    ch = []
    # polygon
    for p in polygon:
        ch.append([p.x, p.y])
        x.append(p.x)
        y.append(p.y)
        #lineas.append([(p.x, p.y), (p[2].x, p[2].y)])

    points = np.array(ch)
    lineas =[]
    for i in range(len(points)-1):
        lineas.append([(points[i][0],points[i][1]), (points[i+1][0], points[i+1][1])])
    lineas.append([(points[-1][0],points[-1][1]), (points[0][0], points[0][1])])

    #orbita
    x1 = []
    y1 = []
    lineas_o = []
    for p in orbita:
        x1.append(p[0].x)
        y1.append(p[0].y)
        lineas_o.append([(p[0].x, p[0].y), (p[2].x, p[2].y)])

    lc_o = mc.LineCollection(lineas_o, linewidths=1)
    lc = mc.LineCollection(lineas, colors="red", linewidths=1)
    fig, ax = plt.subplots()
    
    ax.add_collection(lc_o)
    ax.add_collection(lc)
    ax.margins(0,1)

    # puntos
    plt.scatter(x, y, s=area, c="red", alpha=0.5)
    plt.scatter(x1, y1, s=area, c=colors, alpha=0.5)
    plt.title('Orbit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()



def main(n, r, tipo):
    """
    n -> cantidad de puntos
    r -> rango de valores de los puntos
    tipo -> tipo de orbita a calcular
    """
    if(tipo == "puntos"):
        # Create data
        ps = []
        ps_lista = []
        for x in range(n):
            p_new = point(random.randrange(r), random.randrange(r))
            ps.append(p_new)
            ps_lista.append([p_new.x, p_new.y])
        # plot orbita
        mi_orbita = orbita(ps, point(random.randrange(r), random.randrange(r)), 1)
        dibuja(mi_orbita)
    elif(tipo == "convexo"):
        # Create data
        ps = []
        ps_lista = []
        for x in range(n):
            p_new = point(random.randrange(r), random.randrange(r))
            ps.append(p_new)
            ps_lista.append([p_new.x, p_new.y])

        mi_ch = cierre_convexo(ps_lista)    
        p_inicio = point(random.randrange(20), random.randrange(20))
        #p_inicio = point(25, 1)
        
        print("------------------------")
        print(p_inicio)
        print("------------------------")
        for aux in mi_ch:
            print(str(aux))
        print("------------------------")    
        angulos = calc_tangente(mi_ch, p_inicio)
        print(angulos[0])
        print(angulos[1])
        print("-------------------------")


        mi_orbita = orbita_convexo(mi_ch, p_inicio, 1, "derecha")
        dibuja_convexo(mi_ch, mi_orbita)

    else:
        print("tipo de orbita no valida")




    


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]))

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








