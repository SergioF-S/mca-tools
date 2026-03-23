#!/usr/bin/python3
# paquete que conten funcionalidade para realizar regresions lineais
from numpy import *
from numpy.linalg import * # para determinante matriz
def regresionSimple(x,y):
	"""Axusta os datos dos vectore x e y a unha resta dada pola ec. y=a + bx
	Parametros:
	x vector con medidas da magnitud x
	y vector con medidas da magnitud y
	Devolve:
	a coeficiente a
	b coeficiente b
	sa incerteza de a
	sb incerteza de b
	r coeficiente de regresion lineal """
	n=len(x)
	sx=sum(x); sy=sum(y); xx=dot(x,x); yy=dot(y,y); xy=dot(x,y);
	denom=(n*xx - sx**2)
	b=(n*xy - sx*sy)/denom
	a=(xx*sy - sx*xy)/denom
	s=sqrt(sum((y-a-b*x)**2)/(n-2))
	sa=s*sqrt(xx/(n*xx-sx**2))
	sb=s*sqrt(n/(n*xx-sx**2))
	r=(n*xy-sx*sy)/sqrt((n*xx-sx**2)*(n*yy-sy**2))
	return [a,b, sa, sb, r]
def regresionSimpleSenTermoIndependente(x,y):
	"""Axusta os datos dos vectore x e y a unha resta dada pola ec. y= bx
	Parametros:
	x vector con medidas da magnitud x
	y vector con medidas da magnitud y
	Devolve:
	b coeficiente b
	sb incerteza de b
	r coeficiente de regresion lineal """
	n=len(x)
	xy=dot(x,y); xx=dot(x,x); xy=dot(x,y); yy=dot(y,y)
	b=xy/xx
	s=sqrt(sum((y-b*x)**2)/(n-1))
	sb=s/sqrt(xx)
	r=xy/sqrt(xx*yy)
	return [b, sb, r]
def regresionPonderada(x,y,s):
	"""Axusta os datos dos vectores x e y a unha resta dada pola ec. y=a + bx
	utilizando regresion ponderada
	Parametros:
	x vector con medidas da magnitud x
	y vector con medidas da magnitud y
	s vector coas incertezas na medida y
	Devolve:
	a coeficiente a
	b coeficiente b
	sa incerteza de a
	sb incerteza de b
	r coeficiente de regresion lineal """
	w=1.0/(s*s)
	wy=sum(w*y); wx=sum(w*x);
	wxx=sum(w*x*x); wxy=sum(w*x*y); wyy=sum(w*y*y)
	sw=sum(w)
	d=det(array([[sw, wx],[wx, wxx]]))
	a=(wy*wxx-wx*wxy)/d
	b=(sw*wxy-wx*wy)/d
	sa=sqrt(wxx/d); sb=sqrt(sw/d)
	r=(sw*wxy-wx*wy)/sqrt((sw*wxx-wx**2)*(sw*wyy-wy**2))
	return [a, b, sa, sb, r]
def regresionPonderadaSenTermoIndependente(x,y,s):
	"""Axusta os datos dos vectores x e y a unha resta dada pola ec. y= bx
	utilizando regresion ponderada
	Parametros:
	x vector con medidas da magnitud x
	y vector con medidas da magnitud y
	w vector coas incertezas na medida y
	Devolve:
	b coeficiente b
	sb incerteza de b
	r coeficiente de regresion lineal """
	n=len(x); w=1.0/(s*s); sw=sum(w)
	wxy=sum(w*x*y); wxx=sum(w*x*x); wyy=sum(w*y*y)
	b=wxy/wxx
	s=sqrt(n*sum(w*(y-b*x)**2)/(n-1)/sw)
	sb=1.0/sqrt(wxx)
	r=wxy/sqrt(wxx*wxy)
	return [b, sb, r]
