# -*- encoding: utf-8 -*-
from lxml import etree
import sys
import urllib2
doc=etree.parse('portada.xml')
busqueda = sys.argv[1]
numero_imagenes=doc.xpath("//enclosure") 
if len(sys.argv) > 1:
	#Contains funcion que comprueba si el segundo argumento esta comprendido en el primero
	print "La palabra que desea buscar se ha encontrado %s"%(len(doc.xpath("//*[contains(text(),'%s')]" %busqueda)))
else:
	busqueda=""
print "Numero de noticias o contenido: %s" %(len(doc.xpath("//item")))
print "Numero de imagenes: %s" %(len(numero_imagenes))
for i in numero_imagenes:
	f = urllib2.urlopen(i.get("url"))
	nombre=(i).get("url").split('/')[-1]
	archi=open(nombre,'w')
	archi.write(f.read())
	archi.close()