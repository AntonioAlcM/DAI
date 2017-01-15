import feedparser
import sys
import urllib2

busqueda = sys.argv[1]
if len(sys.argv) < 1:
	busqueda=""
numero_articulos=0
numero_imagenes=0
numero_coincidencias=0
feeds = feedparser.parse(r'portada.xml')
numero_articulos=len(feeds.entries)

for contenido in feeds.entries:
	for img in contenido.enclosures:
		if img.type == "image/jpeg":
			numero_imagenes += 1
			f = urllib2.urlopen(img.url)
			nombre=img.url.split('/')[-1]
			archi=open(nombre,'w')
			archi.write(f.read())
			archi.close()
	if busqueda in contenido.title:
		numero_coincidencias+=1


print "Numero de noticias o contenido: %s" %(numero_articulos)
print "Numero de imagenes: %s" %(numero_imagenes)
print "La palabra que desea buscar se ha encontrado %s"%(numero_coincidencias)