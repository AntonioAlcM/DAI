# -*- encoding: utf-8 -*-
from lxml import etree
import sys
import urllib2


class ParseRssNews ():           # manejadores de eventos
	
	contenido=0
	imagenes=0
	numero_busqueda=0
	if len(sys.argv) < 1:
		busqueda=""
	else:
		busqueda = sys.argv[1] 
	def __init__(self):
		
		print ('--------------------------- Principio del archivo')

	def start(self, tag, attrib):          # Etiquetas de inicio
		print('<%s>' %tag)
		if tag == 'item':
			self.contenido+=1
		if tag == 'enclosure':
			self.imagenes+=1
		for k in attrib:
			if(k=='url'):
				print('%s = "%s"' %(k,attrib[k]))
				f = urllib2.urlopen(attrib[k])
				nombre=attrib[k].split('/')[-1]
				archi=open(nombre,'w')
				archi.write(f.read())
				archi.close()

	def end(self, tag):                    # Etiquetas de fin
		print ('</%s>' %tag)

	def data(self, data):                  # texto
		if self.busqueda in data:
			self.numero_busqueda+=1
		print ('-%s-' %data).encode("UTF8")
			

	def close(self):
		print ('-------------------------------- Fin del archivo')
		print "Numero de noticias o contenido: %s" %(self.contenido)
		print "Numero de imagenes: %s" %(self.imagenes)
		print "La palabra que desea buscar se ha encontrado %s"%(self.numero_busqueda)

parser = etree.XMLParser(target=ParseRssNews())
doc=etree.parse('portada.xml', parser)
