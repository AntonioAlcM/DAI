# -*- encoding: utf-8 -*-
from lxml import etree
import sys
import urllib2

busqueda = sys.argv[1]
if len(sys.argv) < 1:
	busqueda=""
numero_articulos=0
numero_imagenes=0
numero_coincidencias=0
tree = etree.parse('portada.xml')
# Root element
rss = tree.getroot()
# Los elementos funcionan como listas
# First child
channel = rss[0]
for e in channel:
	if (e.tag == 'item'):
		numero_articulos+=1
	for a in e:
		if a.tag=='enclosure' :
			numero_imagenes+=1
			f = urllib2.urlopen(a.get("url"))
			nombre=a.get("url").split('/')[-1]
			archi=open(nombre,'w')
			archi.write(f.read())
			archi.close()
		elif busqueda in a.text:
			numero_coincidencias+=1

			
print "Numero de noticias o contenido: %s" %(numero_articulos)
print "Numero de imagenes: %s" %(numero_imagenes)
print "La palabra que desea buscar se ha encontrado %s"%(numero_coincidencias)
