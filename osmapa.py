# coding: utf-8
import os
import shutil
import re
from ftplib import FTP

#Definiujemy ścieżki i zmienne

data_kompilacji="20170524"

wersja="V1.46"

wersja_szlaki="V1.20"
wersja_mongolia="V1.0"
wersja_fenix_polska="V1.3"
wersja_fenix_topr="V1.2"

wersja_mapy= data_kompilacji + wersja
wersja_mapy_szlaki= data_kompilacji  + wersja
wersja_mapy_mongolia= data_kompilacji + wersja_mongolia
wersja_mapy_fenix_polska= data_kompilacji + wersja
wersja_mapy_fenix_topr= data_kompilacji + wersja

fid_glowna="004"
fid_ogonki="005"
fid_szlaki="006"
fid_light="011"
fid_warstwice="012"
fid_mongolia="21115"
fid_fenix_polska="21116"
fid_fenix_topr="21117"

#overview dla glownej - 007
#overview gla ogonkow - 008
#overview dla mongolii - 009
#overview dla light - 010

styl_mapy_glowna="rogal"
styl_mapy_light="osmapa-light"
styl_mapy_ogonki="rogal"
styl_mapy_szlaki="trasy-rowerowe"
styl_mapy_warstwice="osmapa-warstwice"
styl_mapy_mongolia="mongolia"
styl_mapy_fenix_polska="fenix-polska"
styl_mapy_fenix_topr="fenix-topr"

typfile_glowna="rogal.TYP"                
typfile_ogonki="rogal-ogonki.TYP"
typfile_light="rogal.TYP"   
typfile_szlaki="trasy-rowerowe.TYP"
typfile_mongolia="mongolia.TYP"
typfile_fenix_polska="fenix-polska.typ"
typfile_fenix_topr="fenix-topr.typ"

#SCIEZKI

#bezwzgledna sciezka do katalogu glownego
mapa_root=os.path.abspath("./")


mapy_gotowe= mapa_root + "\\mapy_gotowe" # poziom katalogu z mapami gotowymi wzgledem katalogow w ktorych przeprowadzana jest kompilacja
binarki= mapa_root + "\\bin"

#split i mapy musza byc na tym samym poziomie katalogow

katalog_tmp=mapa_root + "\\tmp"

tmp_dane_osm=mapa_root + "\\OSM"
tmp_mapa_glowna=katalog_tmp + "\\OSMAPA-" + wersja_mapy
tmp_mapa_ogonki=katalog_tmp + "\\OSMAPA-OGONKI-" + wersja_mapy 
tmp_mapa_light=katalog_tmp + "\\OSMAPA-LIGHT-" + wersja_mapy 
tmp_mapa_szlaki=katalog_tmp + "\\OSMAPA-SZLAKI" + wersja_mapy_szlaki
tmp_mapa_warstwice=katalog_tmp + "\\OSMAPA-WARSTWICE"
tmp_mapa_mongolia=katalog_tmp + "\\MONGOLIA-TOPO" + wersja_mapy_mongolia
tmp_mapa_fenix_polska=katalog_tmp + "\\FENIX-POLSKA" + wersja_mapy_fenix_polska
tmp_mapa_fenix_topr=katalog_tmp + "\\FENIX-TOPR" + wersja_mapy_fenix_topr

tmp_mapa_split_glowna=katalog_tmp + "\\OSM-Poland-split-glowna"
tmp_mapa_split_ogonki=katalog_tmp + "\\OSM-Poland-split-ogonki"
tmp_mapa_split_light=katalog_tmp + "\\OSM-Poland-split-light"
tmp_mapa_split_szlaki=katalog_tmp + "\\OSM-Poland-split-szlaki"
tmp_mapa_split_warstwice=katalog_tmp + "\\OSM-Poland-split-warstwice"
tmp_mapa_split_fenix_polska=katalog_tmp + "\\OSM-Poland-split-fenix"
tmp_mapa_split_fenix_topr=katalog_tmp + "\\OSM-Poland-split-fenix-topr"
tmp_mapa_split_mongolia=katalog_tmp + "\\OSM-Mongolia-split"



def pobierz_dane_osm():

  try:
    os.remove(tmp_dane_osm + '/europe-latest.osm.pbf')
  except:
    pass
  
  #print '{binarki}\\wget.exe -c http://download.geofabrik.de/europe-latest.osm.pbf -o {t}/europe-latest.osm.pbf'.format(binarki=binarki, tmp=tmp_dane_osm)
  ret=os.system('{binarki}\\wget.exe -c http://download.geofabrik.de/europe-latest.osm.pbf -t 5  -O {dane_osm}/europe-latest.osm.pbf'.format(binarki=binarki, dane_osm=tmp_dane_osm))

  if(ret!=0):
    raise Exception("Blad pobierania danych OSM")
    
    
def pobierz_dane_mongolia():

  try:
    os.remove(tmp_dane_osm + '/mongolia-latest.osm.pbf')
  except:
    pass
  
  ret=os.system('{binarki}\\wget.exe -c http://download.geofabrik.de/asia/mongolia-latest.osm.pbf -t 5  -O {dane_osm}/mongolia-latest.osm.pbf'.format(binarki=binarki, dane_osm=tmp_dane_osm))

  if(ret!=0):
    raise Exception("Blad pobierania danych OSM")



def wydziel_obszar():
 
  ret=os.system('{binarki}\\osmosis\\bin\\\osmosis.bat --rb {dane_osm}\\europe-latest.osm.pbf --bounding-polygon file={dane_osm}\\polska_przygranicze.poly --wb {dane_osm}\\poland.extract.osm.pbf'.format(binarki=binarki, dane_osm=tmp_dane_osm))
    
  if(ret!=0):
    raise Exception("Blad ekstrakcji danych OSM")
    
def wydziel_obszar_topr():
 
  ret=os.system('{binarki}\\osmosis\\bin\\\osmosis.bat --rb {dane_osm}\\europe-latest.osm.pbf --bounding-polygon file={dane_osm}\\topr.poly --wb {dane_osm}\\topr.extract.osm.pbf'.format(binarki=binarki, dane_osm=tmp_dane_osm))
    
  if(ret!=0):
    raise Exception("Blad ekstrakcji danych OSM")    
    

def split_mapy(dest, fid):

  os.chdir(dest)
  
  try:
    for f in os.listdir("."):
      os.remove(f)
  except:
    pass

 
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid=66{fid}001 --max-nodes=1600000 {dane_osm}\\poland.extract.osm.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) )
   
    
  if(ret!=0):
    raise Exception("Blad splitowania danych OSM")
    
    
def split_mapy_szlaki(dest, fid):

  os.chdir(dest)
  
  try:
    for f in os.listdir("."):
      os.remove(f)
  except:
    pass

 
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid=66{fid}001 --max-nodes=1600000 {dane_osm}\\poland.extract.osm.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) )
  #ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid=66{fid}001 --max-nodes=1600000  {dane_osm}\\srtm_polska.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) ) 
    
  if(ret!=0):
    raise Exception("Blad splitowania danych OSM")
    
def split_mapy_warstwice(dest, fid):

  os.chdir(dest)
  
  try:
    for f in os.listdir("."):
      os.remove(f)
  except:
    pass

 
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid=66{fid}001 --max-nodes=1600000  {dane_osm}\\srtm_polska.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) )
  #ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid=66{fid}001 --max-nodes=1600000  {dane_osm}\\srtm_polska.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) ) 
    
  if(ret!=0):
    raise Exception("Blad splitowania danych OSM")
        
    
    
def split_mapy_mongolia(dest, fid):

  os.chdir(dest)
  
  try:
    for f in os.listdir("."):
      os.remove(f)
  except:
    pass

 
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid={fid}001 --max-nodes=1600000 {dane_osm}\\mongolia-latest.osm.pbf {dane_osm}\\srtm_mongolia.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) )
   
    
  if(ret!=0):
    raise Exception("Blad splitowania danych OSM")
    
def split_mapy_fenix(dest, fid):

  os.chdir(dest)
  
  try:
    for f in os.listdir("."):
      os.remove(f)
  except:
    pass

 
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid={fid}001 --max-nodes=1600000 {dane_osm}\\poland.extract.osm.pbf'.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) )
   
    
  if(ret!=0):
    raise Exception("Blad splitowania danych OSM")
    

def split_mapy_fenix_topr(dest, fid):

  os.chdir(dest)
  
  try:
    for f in os.listdir("."):
      os.remove(f)
  except:
    pass

 
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}\\splitter.jar --keep-complete=true --mapid={fid}001 --max-nodes=1600000 {dane_osm}\\srtm_topr.pbf {dane_osm}\\topr.extract.osm.pbf '.format(mapa_root=mapa_root,dane_osm=tmp_dane_osm, fid=fid, binarki=binarki) )
   
    
  if(ret!=0):
    raise Exception("Blad splitowania danych OSM")
    



def generuj_granice():

  ret=os.system("start /low /b /wait {binarki}\\osmconvert.exe {dane_osm}\\poland.extract.osm.pbf --out-o5m >{dane_osm}\\poland.o5m".format(binarki=binarki, dane_osm=tmp_dane_osm))
  ret=os.system("start /low /b /wait {binarki}\\osmfilter.exe {dane_osm}\\poland.o5m --keep-nodes= --keep-ways-relations=\"boundary=administrative =postal_code postal_code=\" >{dane_osm}\\poland-boundaries.osm".format(dane_osm=tmp_dane_osm, binarki=binarki))
  ret=os.system("start /low /b /wait java -cp {binarki}\\mkgmap.jar uk.me.parabola.mkgmap.reader.osm.boundary.BoundaryPreprocessor {dane_osm}\\poland-boundaries.osm {dane_osm}\\bounds".format(binarki=binarki, dane_osm=tmp_dane_osm))

def generuj_granice_mongolia():

  ret=os.system("start /low /b /wait {binarki}\\osmconvert.exe {dane_osm}\\mongolia-latest.osm.pbf --out-o5m >{dane_osm}\\mongolia.o5m".format(binarki=binarki, dane_osm=tmp_dane_osm))
  ret=os.system("start /low /b /wait {binarki}\\osmfilter.exe {dane_osm}\\mongolia.o5m --keep-nodes= --keep-ways-relations=\"boundary=administrative =postal_code postal_code=\" >{dane_osm}\\mongolia-boundaries.osm".format(dane_osm=tmp_dane_osm, binarki=binarki))
  ret=os.system("start /low /b /wait java -cp {binarki}\\mkgmap.jar uk.me.parabola.mkgmap.reader.osm.boundary.BoundaryPreprocessor {dane_osm}\\mongolia-boundaries.osm {dane_osm}\\bounds-mongolia".format(binarki=binarki, dane_osm=tmp_dane_osm))




#dest - katalog tymczasowy kompilacji, source - katalog z danymi split
def przygotuj_kompilacje(dest, source):

  try:
    print("Usuwanie zawartosci katalogu: " + dest)
    shutil.rmtree(dest, True)

  except Exception:
    pass
    
  os.mkdir(dest)
 
    
  print("Kopiowanie danych zrodlowych (split) do folderu " + dest)
    
  if(len(os.listdir(source))==0):
    raise Exception("Katalog {source} jest niedostepny lub pusty!".format(source=source) )
    
  for plik in os.listdir(source):
    shutil.copy(source + "/" + plik, dest)


def kompiluj_mape_glowna():
 
  os.chdir(tmp_mapa_glowna)
  shutil.copy(binarki + "/typ/" + typfile_glowna, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --verbose --family-name=OSMapaPL --description=OSMapaPL --series-name=OSMapaPL  --coastlinefile={dane_osm}/coastlines_europe.osm.pbf  --read-config={mapa_root}/config/osmapa.config --bounds={dane_osm}/bounds --family-id={fid_glowna} --product-id={fid_glowna} --mapname=66{fid_glowna}001 --overview-mapname=66{fid_glowna}000   --style-file={binarki}/resources/styles/ --style={styl}  --check-styles  -c template.args  style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_glowna, fid_glowna=fid_glowna, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 66004000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/OSMapaPL-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  except:
      pass
      
  os.rename("OSMapaPL.exe", "{mapy_gotowe}/OSMapaPL-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\OSMapaPL-{wersja_mapy}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_glowna, True)
  
  
  
def kompiluj_mape_warstwice():
 
  os.chdir(tmp_mapa_warstwice)
  #shutil.copy(binarki + "/typ/" + typfile_glowna, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --verbose --family-name=OSMapa-warstwice --description=OSMapa-warstwice --series-name=OSMapa-warstwice    --read-config={mapa_root}/config/osmapa_warstwice.config  --family-id={fid_warstwice} --product-id={fid_warstwice} --mapname=66{fid_warstwice}001 --overview-mapname=66{fid_warstwice}000   --style-file={binarki}/resources/styles/ --style={styl}  --check-styles  -c template.args'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_warstwice, fid_warstwice=fid_warstwice, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 66012000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/OSMapa-warstwice.exe".format(mapy_gotowe=mapy_gotowe))
  except:
      pass
      
  os.rename("OSMapa-warstwice.exe", "{mapy_gotowe}/OSMapa-warstwice.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\OSMapa-warstwice_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_warstwice, True)
    
  
  
def kompiluj_mape_fenix_polska():
 
  os.chdir(tmp_mapa_fenix_polska)
  shutil.copy(binarki + "/typ/" + typfile_fenix_polska, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --verbose --family-name=OSMapaPL-Fenix --description=OSMapaPL-Fenix --series-name=OSMapaPL-Fenix    --read-config={mapa_root}/config/fenix_polska.config --bounds={dane_osm}/bounds --family-id={fid_fenix_polska} --product-id={fid_fenix_polska} --mapname={fid_fenix_polska}001 --overview-mapname={fid_fenix_polska}000   --style-file={binarki}/resources/styles/ --style={styl}  --check-styles -c template.args    style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_fenix_polska, fid_fenix_polska=fid_fenix_polska, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 21116000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/OSMapaPL-Fenix-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy_fenix_polska))
  except:
      pass
      
  os.rename("OSMapaPL-Fenix.exe", "{mapy_gotowe}/OSMapaPL-Fenix-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy_fenix_polska))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\OSMapaPL-Fenix-{wersja_mapy}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy_fenix_polska, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_fenix_polska, True)
  

  
def kompiluj_mape_fenix_topr():
 
  os.chdir(tmp_mapa_fenix_topr)
  shutil.copy(binarki + "/typ/" + typfile_fenix_topr, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --verbose --family-name=Fenix-TOPR --description=Fenix-TOPR --series-name=Fenix-TOPR    --read-config={mapa_root}/config/fenix_topr.config --bounds={dane_osm}/bounds --family-id={fid_fenix_topr} --product-id={fid_fenix_topr} --mapname={fid_fenix_topr}001 --overview-mapname={fid_fenix_topr}000   --style-file={binarki}/resources/styles/ --style={styl}  --check-styles -c template.args    style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_fenix_topr, fid_fenix_topr=fid_fenix_topr, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 21117000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/Fenix-TOPR-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy_fenix_topr))
  except:
      pass
      
  os.rename("Fenix-TOPR.exe", "{mapy_gotowe}/Fenix-TOPR-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy_fenix_topr))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\Fenix-TOPR-{wersja_mapy}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy_fenix_topr, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_fenix_topr, True)  
  
  
def kompiluj_mape_ogonki():
 
  os.chdir(tmp_mapa_ogonki)
  shutil.copy(binarki + "/typ/" + typfile_ogonki, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --family-name=OSMapaPL-OGONKI --description=OSMapaPL-OGONKI --series-name=OSMapaPL-OGONKI  --coastlinefile={dane_osm}/coastlines_europe.osm.pbf  --read-config={mapa_root}/config/osmapa_ogonki.config --bounds={dane_osm}/bounds --family-id={fid_ogonki} --product-id={fid_ogonki} --mapname=66{fid_ogonki}001 --overview-mapname=66{fid_ogonki}000  --style-file={binarki}/resources/styles/ --style={styl} --check-styles --lower-case --code-page=1250  -c template.args  style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_ogonki, fid_ogonki=fid_ogonki, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 66005000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/OSMapaPL-OGONKI-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  except:
      pass
      
  os.rename("OSMapaPL-OGONKI.exe", "{mapy_gotowe}/OSMapaPL-OGONKI-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\OSMapaPL-OGONKI-{wersja_mapy}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_ogonki, True)
  
  
def kompiluj_mape_light():
 
  os.chdir(tmp_mapa_light)
  shutil.copy(binarki + "/typ/" + typfile_light, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --family-name=OSMapaPL-LIGHT --description=OSMapaPL-LIGHT --series-name=OSMapaPL-LIGHT  --coastlinefile={dane_osm}/coastlines_europe.osm.pbf  --read-config={mapa_root}/config/osmapa_light.config --bounds={dane_osm}/bounds --family-id={fid_ogonki} --product-id={fid_ogonki} --mapname=66{fid_ogonki}001 --overview-mapname=66{fid_ogonki}000  --style-file={binarki}/resources/styles/ --style={styl} --check-styles  -c template.args  style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_light, fid_ogonki=fid_light, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 66011000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/OSMapaPL-LIGHT-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  except:
      pass
      
  os.rename("OSMapaPL-LIGHT.exe", "{mapy_gotowe}/OSMapaPL-LIGHT-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\OSMapaPL-LIGHT-{wersja_mapy}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_light, True)  
  
  
def kompiluj_mape_szlaki():
 
  os.chdir(tmp_mapa_szlaki)
  shutil.copy(binarki + "/typ/" + typfile_szlaki, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -Dlog.config={binarki}/mkgmap_log.props -enableassertions -Xmx2000m -jar {binarki}/mkgmap.jar  --family-name=OSMapaPL-SZLAKI  --read-config={mapa_root}/config/osmapa_szlaki.config  --family-id={fid_szlaki} --product-id={fid_szlaki} --mapname=66{fid_szlaki}001 --overview-mapname=66{fid_szlaki}000 --description=OSMapaPL-SZLAKI --series-name=OSMapaPL-SZLAKI  --style-file={binarki}/resources/styles/ --style={styl}  --check-styles -c template.args  style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_szlaki, fid_szlaki=fid_szlaki, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 66006000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/OSMapaPL-SZLAKI-{wersja_mapy_szlaki}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy_szlaki=wersja_mapy_szlaki))
  except:
      pass
      
  os.rename("OSMapaPL-SZLAKI.exe", "{mapy_gotowe}/OSMapaPL-SZLAKI-{wersja_mapy_szlaki}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy_szlaki=wersja_mapy_szlaki))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\OSMapaPL-SZLAKI-{wersja_mapy_szlaki}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy_szlaki=wersja_mapy_szlaki, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_szlaki, True)  
  
  
  
def kompiluj_mape_mongolia():
 
  os.chdir(tmp_mapa_mongolia)
  shutil.copy(binarki + "/typ/" + typfile_mongolia, "style.typ") 
  shutil.copy(mapa_root + "/README.TXT", "README.TXT")
  ret=os.system('start /low /b /wait java -enableassertions -Xmx6000m -jar {binarki}/mkgmap.jar --verbose --family-name=Mongolia-Topo --description=Mongolia-Topo --series-name=Mongolia-Topo --read-config={mapa_root}/config/mongolia.config --bounds={dane_osm}/bounds-mongolia --family-id={fid_mongolia} --product-id={fid_mongolia} --mapname={fid_mongolia}001 --overview-mapname={fid_mongolia}000   --style-file={binarki}/resources/styles/ --style={styl}  --check-styles  -c template.args  style.typ'.format(mapa_root=mapa_root, binarki=binarki, styl=styl_mapy_mongolia, fid_mongolia=fid_mongolia, dane_osm=tmp_dane_osm))    
  print("kompiluj_mape_mongolia - mkgmap return value: " + str(ret))


  ret=os.system("start /low /b /wait {binarki}\\NSIS\\makensis.exe 21115000.nsi".format(binarki=binarki))

  print("nsis - ret: " + str(ret))
  
  if(ret!=0):
    raise Exception("Blad kompilatora NSIS")
  
  try:
      os.remove("{mapy_gotowe}/Mongolia-Topo-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy_mongolia))
  except:
      pass
      
  os.rename("Mongolia-Topo.exe", "{mapy_gotowe}/Mongolia-Topo-{wersja_mapy}.exe".format(mapy_gotowe=mapy_gotowe, wersja_mapy=wersja_mapy_mongolia))
  
  ret=os.system("start /low /b /wait {binarki}\\zip.exe -9 {mapy_gotowe}\\Mongolia-Topo-{wersja_mapy}_IMG.zip gmapsupp.img README.TXT".format(binarki=binarki, wersja_mapy=wersja_mapy_mongolia, mapy_gotowe=mapy_gotowe))    

  if(ret!=0):
    raise Exception("Blad kompresora ZIP")

  os.chdir(mapa_root)
  
  shutil.rmtree(tmp_mapa_mongolia, True)
    
  

#def upload_map():

#  os.chdir(mapy_gotowe)
  #file=open('OSMapaPL-{wersja_mapy}.exe'.format(wersja_mapy=wersja_mapy, 'rb')
  #ftp.storbinary()
  
  #ftp.login()



if __name__=="__main__":

# OSMAPA

  pobierz_dane_osm()
  wydziel_obszar()
  wydziel_obszar_topr()
  
  #tego nie odkomentowywac!!!!
  #generuj_granice()
  
  
  split_mapy(tmp_mapa_split_glowna, fid_glowna)
  split_mapy(tmp_mapa_split_ogonki, fid_ogonki)
  split_mapy(tmp_mapa_split_light, fid_light)
  split_mapy_fenix(tmp_mapa_split_fenix_polska, fid_fenix_polska)
  split_mapy_fenix_topr(tmp_mapa_split_fenix_topr, fid_fenix_topr)
  split_mapy_szlaki(tmp_mapa_split_szlaki, fid_szlaki) 
  
  #split_mapy_warstwice(tmp_mapa_split_warstwice, fid_warstwice) 
  
  #przygotuj_kompilacje(tmp_mapa_warstwice, tmp_mapa_split_warstwice)
  #kompiluj_mape_warstwice()
  
  przygotuj_kompilacje(tmp_mapa_glowna, tmp_mapa_split_glowna)
  kompiluj_mape_glowna()
  
  przygotuj_kompilacje(tmp_mapa_ogonki, tmp_mapa_split_ogonki)
  kompiluj_mape_ogonki()

  przygotuj_kompilacje(tmp_mapa_light, tmp_mapa_split_light)
  kompiluj_mape_light()
 
  przygotuj_kompilacje(tmp_mapa_szlaki, tmp_mapa_split_szlaki)
  kompiluj_mape_szlaki()
  
  przygotuj_kompilacje(tmp_mapa_fenix_polska, tmp_mapa_split_fenix_polska)
  kompiluj_mape_fenix_polska()
 
  przygotuj_kompilacje(tmp_mapa_fenix_topr, tmp_mapa_split_fenix_topr)
  kompiluj_mape_fenix_topr()
  
  #upload_map()


# MONGOLIA

#  pobierz_dane_mongolia()
#  split_mapy_mongolia(tmp_mapa_split_mongolia, fid_mongolia)
#  generuj_granice_mongolia()
#  przygotuj_kompilacje(tmp_mapa_mongolia, tmp_mapa_split_mongolia)
#  kompiluj_mape_mongolia()
  
  

