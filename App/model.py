"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import shellsort as she
from DISClib.Algorithms.Sorting import selectionsort as sel
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Sorting import quicksort as qui


assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


def newCatalog():
    catalog = {'videos': None,
               'country': None,
               'category': None,
               'tags': None}

    catalog['videos'] = lt.newList(datastructure="ARRAY_LIST",
                                   cmpfunction=compVideosByViews)
    catalog['country'] = mp.newMap(numelements=17,
                                prime=109345121,
                                maptype='CHAINING',
                                loadfactor=0.5,
                                comparefunction=None)
    catalog['category'] = mp.newMap(numelements=17,
                                prime=109345121,
                                maptype='CHAINING',
                                loadfactor=0.5,
                                comparefunction=None)
    return catalog

def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)

def addVideoCountry(catalog, video,contador):
    countryname = video["country"]
    countries = catalog['country']
    if mp.contains(countries,countryname):
        l = mp.get(countries,countryname)["value"]
        l.append(contador)
        mp.put(countries,countryname,l)
    else:
        l=[contador]
        mp.put(countries,countryname,l)
        

def addVideoCategory(catalog, video,contador):
    categoryidnu = video["category_id"]
    categories = catalog['category']
    name = None
    categoryfile = cf.data_dir + 'Videos/category-id.csv'
    with open(categoryfile, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile,delimiter="\t")
        for row in reader:
            if row['id'] ==categoryidnu :
                name = row['name']
                break

    if mp.contains(categories,name):
        l = mp.get(categories,name)["value"]
        l.append(contador)
        mp.put(categories,name,l)
    else:
        l=[contador]
        mp.put(categories,name,l)


def newSList(lst, pos, numelem):
    return lt.subList(lst, pos, numelem)




# Funciones para creacion dzae datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compVideosByViews(video1,video2):
    if int(video1["views"]) > int(video2["views"]):
        return True
    else:
        return False 

def compVideosByLikes(video1,video2):
    if int(video1["likes"]) > int(video2["likes"]):
        return True
    else:
        return False 
# Funciones de ordenamiento

def sortViews(lst, fun):
    if fun == "shellsort":
        return shesort(lst,compVideosByViews)
    elif fun == "mergesort":
        return mergesort(lst,compVideosByViews)
    elif fun == "quicksort":
        return quicksort(lst,compVideosByViews)
    elif fun == "selectionsort":
        return selesort(lst,compVideosByViews)
    else:
        print("Funcion de ordenamiento no existe.")

def sortLikes(lst, fun):
    if fun == "shellsort":
        return shesort(lst,compVideosByLikes)
    elif fun == "mergesort":
        return mergesort(lst,compVideosByLikes)
    elif fun == "quicksort":
        return quicksort(lst,compVideosByLikes)
    elif fun == "selectionsort":
        return selesort(lst,compVideosByLikes)
    else:
        print("Funcion de ordenamiento no existe.")

def selesort(lst,cmpfunction):
    return sel.sort(lst, cmpfunction)

def insersort(lst,cmpfunction):
    return ins.sort(lst, cmpfunction)

def shesort(lst,cmpfunction):
    return she.sort(lst, cmpfunction)

def quicksort(lst,cmpfunction):
    return qui.sort(lst, cmpfunction)

def mergesort(lst,cmpfunction):
    return mer.sort(lst, cmpfunction)

def videosTrending(country,category,catalog):
    videos= findVideos(country,category,catalog)
    return videos


def findVideos(country,category,catalog):
    countries= catalog['country']
    categories = catalog['category']
    l = mp.get(countries,country)['value']
    c = mp.get(categories,category)['value']
    lf=[]
    for u in l:
        if u in c:
            lf.append(u)
    v=idTranslate(lf,catalog['videos'])
    return v

def idTranslate(ids,videos):
    v=lt.newList(datastructure='ARRAY_LIST',cmpfunction=compVideosByViews)
    for i in ids:
        lt.addLast(v,lt.getElement(videos,i))
    return v

def presantacion(l):
    newIterator=lt.iterator(l)
    for i in newIterator:
        print('Trending Date: '+str(i['trending_date'])+'\t''Title: '+i['title']+'\t'+'Channel Title: '+i['channel_title']+'\t'+'Publish Time: '+str(i['publish_time'])+'\t'+'Views: '+i['views']+'\t'+'Likes: '+i['likes']+'\t'+'Dislikes: '+i['dislikes']+'\n'+'\n')

def tagsEsp(country,tag,catalog):
    video=catalog['videos']
    countries=catalog['country']
    l = mp.get(countries,country)['value']
    r=[]
    for u in l:
        v=lt.getElement(video,u)
        y=v['tags']
        if tag in y:
            r.append(u)
    ra=idTranslate(r,video)
    return ra

def presantacionTag(l):
    newIterator=lt.iterator(l)
    for i in newIterator:
        print('Title: '+i['title']+'\t'+'Channel Title: '+i['channel_title']+'\t'+'Publish Time: '+str(i['publish_time'])+'\t'+'Views: '+i['views']+'\t'+'Likes: '+i['likes']+'\t'+'Dislikes: '+i['dislikes']+'\t'+'Tags: '+i['tags']+'\n'+'\n')


def duracionTen(country,catalog):
    videos=catalog['videos']
    c= catalog['country']
    z = mp.get(c,country)['value']
    d=mp.newMap(numelements=1)
    for x in z:
        t=lt.getElement(videos,x)
        if mp.contains(d,t['video_id']):
            v=mp.get(d,t['video_id'])['value']
            v+=1
            mp.put(d,t['video_id'],v)
        else:
            mp.put(d,t['video_id'],1)
    temp= None
    mayor = 0
    keySet= mp.keySet(d)
    iterator=lt.iterator(keySet)
    for k in iterator:
        tv=mp.get(d,k)['value']
        if tv > mayor:
            mayor= tv
            temp =k
    for y in z:
        t=lt.getElement(videos,y)
        if t['video_id']==temp:
            lr=[t['title'],t['channel_title'],t['country'],mayor]
            return lr

def presentacionReq2(lr):
    print('Titulo: '+lr[0]+'\n'+'Nombre del canal: '+lr[1]+'\n'+'Pais: '+lr[2]+'\n'+'Dias: '+str(lr[3]))

    

    








    


    





