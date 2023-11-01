#Viviane Binet - Timothée Maviel
#20 décembre 2022



# Ce programme lance une variante simplifiée du jeu de démineur sur la page
# Web de Codeboot.



mines= 4  #nombre de mines dans le jeu
grilleChiffres=[] #pour créer le tableau qui contient les mines et les chiffres
grilleAfficher = []  #pour afficher les tuiles peu à peu dans le jeu


import functools


####  Créer le tableau des mines et des chiffres  ####


# La fonction image prend en paramètre un texte qui est le nom de l'image 
# que la fonction convertit en format de texte qui est un lien vers la source
# de l'image sur le Web, pour pouvoir l'afficher sur la page Web.

def image(element):
    return ('<img src="http://codeboot.org/images/minesweeper/'+ str(element)
            + '.png">')



# Les fonctions table, tr et td prennent en paramètre un texte qui est le 
# contenu de la table, de la rangée ou de la cellule. Ces fonctions retournent
# un texte qui est le contenu sous le bon format HTML pour créer un tableau.

def table(contenu): return '<table>' + contenu + '</table>'
def tr(contenu): return '<tr>' + contenu + '</tr>'
def td(contenu, idCase, largeur, hauteur): 
    return '<td id="case'+str(idCase)+'"  onclick= "clic('+ str(idCase) + \
           ', event.shiftKey,'+ str(largeur) + ',' + str(hauteur) +  \
           ')">' + contenu  +'</td>'



# La fonction creerGrille prend en paramètres deux entiers positifs qui sont
# le nombre de cases de largeur et de hauteur de la grille de jeu. Elle 
# retourne un tableau qui contient (largeur*hauteur) textes d'images de 
# cases 'blank'.

def creerGrille(largeur, hauteur):
    taille = hauteur * largeur
    grille = []
    
    for i in range(taille):
        grille.append(image("blank"))
 
    return grille



# La fonction tab2Html prend en paramètre un tableau de tableaux  qui sont les
# éléments d'une grille avec des coordonnées (i), et retourne un texte
# qui décrit cette grille dans le format HTML.

def tab2Html(tableau, largeur, hauteur):
    tab=""
    for y in range (hauteur):  #créer une rangée
        ligne=""
        for  x in range (largeur):  #créer chaque cellule dans la rangée
            ligne+=td(tableau[x+y*largeur], x+y*largeur, largeur, hauteur )
            
            
        tab+= tr(ligne)
    
    #donne le code HTML de la grille qui contient les tuiles blank
    tableau1= table(tab) 
    
    return tableau1 



# La fonction placerMines prend en paramètres 4 entiers positifs. Le premier
# est la quantité de mines à placer dans le jeu, les deuxième et troisième
# sont la largeur et la hauteur de la grille, et le quatrième est la position
# de la case qui ne doit pas contenir de mine (la première case cliquée). 
# Cette fonction retourne un tableau qui contient les textes d'images
# d'une grille avec des mines placées aléatoirement et le reste des cases
# sont 'blank'.

def placerMines(quantite, largeur, hauteur, exclu):
    grille= creerGrille(largeur, hauteur)
    compteur = 0
    for i in range (quantite):
        grille[i]=image("mine")
    
    for i in range (len(grille)-1):    # Algorithme de mélange de Fisher-Yates
        j = math.floor(random()*i)
        a=grille[i]
        grille[i]=grille[j]
        grille[j]=a
        
        #échanger la case exclue avec la dernière case (sans mine)
        if grille[exclu]==image("mine"):
            grille[-1]= image("mine")
            grille[exclu]= image("blank")
    
    return(grille)
    

    
# La fonction trouverCasesAutour prend en paramètres un tableau de textes
# d'images, deux entiers positifs qui sont la largeur et la hauteur de la 
# grille, et un entier positif qui est la position de la case autour de 
# laquelle on veut trouver les autres cases. Cette fonction retourne un 
# tableau des positions de toutes les cases autour de la case de position i.

def trouverCasesAutour(grille, largeur, hauteur, i):
     # tableau des positions des 8 cases entourant la case i
        voisins1=[i+1, i+1+largeur, i+largeur, i-1+largeur, i-1, i-1-largeur, 
            i-largeur, i+1-largeur]
        voisins= voisins1*2  # pour éviter les indexs hors du tableau
        
        #positions des cases dans les coins
        coins= [0, largeur-1, largeur*hauteur-1, largeur*(hauteur-1)]
     
        for j in range(len(coins)):
            if coins[j]==i:
                autour = voisins[2*j:2*j+3]
                return autour
             
       
        #positions des cases aux bordures
        bordures=[i<largeur, (i+1)%largeur==0, i>= largeur*(hauteur-1), 
                  i%largeur==0]
               
        for j in range (len(bordures)):
            if bordures[j]:
                autour=voisins[2*j:2*j+5]
                return autour
            
        
        autour= voisins1   #au centre
        return autour
        


# La fonction compterMines prend en paramètre un tableau qui contient des 
# textes représentant les images affichées dans chaque case de la grille 
# (forme tab[i]) qui contient des mines, ainsi que la largeur et la hauteur
# de ce tableau (nombres  entiers positifs). Elle retourne un tableau du 
# même format que celui d'entrée, mais dont certaines cases contiennent des
# chiffres qui indiquent le nombre de mines à proximité.

def compterMines(grille, largeur, hauteur):
    grilleNombres=[]
    
    
    for i in range (hauteur*largeur):
        autour=trouverCasesAutour(grille, largeur, hauteur, i)
        casesAutour= list(map(lambda j : grille[j] , autour))
        
        #compter combien de mines sont dans les cases autour
        nbMines= functools.reduce(lambda n, m: n+ (m==image("mine")), 
                                  casesAutour,0)
        
        
        #ajouter ces nombres à la grille de jeu
        grilleNombres.append(image(nbMines)) if grille[i]!= image("mine") \
                                   else grilleNombres.append(image("mine"))
       
   
    return grilleNombres






####  Dévoiler les tuiles récursivement  ####


# La fonction devoilerTuiles prend en paramètre 3 entiers positifs. Le premier
# est la position de la case à laquelle s'applique la fonction. Les 2 autres
# sont la largeur et la hauteur de la grille de jeu. Cette fonction trouve
# les cases autour de la case d'origine et les dévoile si elles sont vides,
# ou si ce sont des cases avec des chiffres accolées aux cases vides
# Elle retourne la position de la case dévoilée.

def devoilerTuiles(case, largeur, hauteur):
   
    global grilleAfficher
    casesAutour = trouverCasesAutour(grilleChiffres, largeur, hauteur, case)
    
    for i in casesAutour:
        if grilleChiffres[i] == image(0):
            devoiler(i, largeur, hauteur)
       
        if grilleChiffres[i] != image("mine"):
            casesAutour2 = trouverCasesAutour(grilleChiffres, 
                                              largeur, hauteur, i)
            
            for j in casesAutour2:
                if grilleAfficher[j] == image(0):
                    devoiler(i, largeur, hauteur)
  
    return case



# La fonction devoiler prend en paramètres 3 entiers positifs qui représentent
# les mêmes éléments que pour la fonction devoilerTuiles. Elle change le 
# contenu du tableau grilleAfficher pour dévoiler les tuiles qui ne contiennent
# pas de mines, et appelle devoilerTuiles pour appliquer le même processus aux
# cases autour. Elle retourne le tableau grilleAfficher modifié.

def devoiler(case, largeur, hauteur):
    global grilleAfficher, grilleChiffres
    
    if grilleAfficher[case] == image("blank"):
        grilleAfficher[case] = grilleChiffres[case]
        
        if grilleChiffres[case] == image(0):
            devoilerTuiles(case, largeur, hauteur)
    
    return grilleAfficher
    
    



    
####  Réagir lorsqu'une case est cliquée  ####
    

# La fonction element prend en paramètre un texte qui est l'id d'un élément 
# du DOM et retourne cet élément sélectionné. La fonction case prend en 
# paramètre un entier positif qui est la position de la case et retourne cette
# case sélectionnée. Ces deux fonctions proviennent des notes de cours.

def element(id):
    return document.querySelector('#' + id)
def case(index):
    return element('case' + str(index))



# La procédure clic prend en paramètres un entier positif qui est la position
# de la case cliquée, un booléen qui indique si la touche 'shift' est appuyée
# lors du clic, et 2 entiers positifs qui sont la largeur et la hauteur de la
# grille. Cette procédure modifie la grille qui est affichée à l'écran ainsi
# que le tableau grilleAfficher qui garde en mémoire les cases dévoilées, 
# selon le clic qui est fait sur la grille. Lors du premier clic, elle 
# construit le tableau grilleChiffres en plaçant les mines aléatoirement.
# Elle détermine aussi si la partie est gagnée ou perdue et l'affiche. 

def clic(idCase, shift, largeur, hauteur):
    
    global grilleChiffres, mines, grilleAfficher
    if shift:
        if case(idCase).innerHTML==image("flag"): #si il y a déjà un drapeau
            case(idCase).innerHTML=image("blank")
            grilleAfficher[idCase]=image("blank")
        else:
            case(idCase).innerHTML=image("flag")
            grilleAfficher[idCase]=image("flag")
        
    else:
        #Si c'est le premier clic, on veut s'assurer que ce n'est pas une mine
        if grilleAfficher==[image("blank")]*len(grilleAfficher):
            grilleChiffres= compterMines(placerMines (mines, largeur,
                     hauteur, idCase), largeur, hauteur)
            
        if grilleAfficher[idCase]==image("flag"): #protéger la tuile
            pass
   

        elif grilleChiffres[idCase]==image("mine"): #la partie est perdue
            
            for i in range(len(grilleChiffres)):
                if grilleChiffres[i]==image("mine"):
                    case(i).innerHTML=image("mine")
                
                elif case(i).innerHTML==image("flag"):
                    case(i).innerHTML=image("mine-red-x")
            
            case(idCase).innerHTML=image("mine-red")
            sleep(0.5)
            alert("Vous avez perdu!")
            init(largeur, hauteur)
            
        else:    
            case(idCase).innerHTML=grilleChiffres[idCase]
            tab=devoiler(idCase, largeur, hauteur)
            for i in range(len(grilleChiffres)):
                case(i).innerHTML=tab[i]
            
            #on veut savoir si le joueur a gagné
            compteur=0   #combien de tuiles sont retournées?
            for i in range(len(grilleChiffres)):
                if case(i).innerHTML!=image("blank") \
                    and case(i).innerHTML!=image("flag"):
                    compteur+=1
            
            if len(grilleChiffres)-compteur==mines:
           
           #dévoiler les cases où il y a des mines qui n'ont pas été dévoilées
                for i in range(len(grilleChiffres)):
                    if (case(i).innerHTML==image("blank") 
                        and grilleChiffres[i]==image("mine")):
                        case(i).innerHTML=image("mine")
                sleep(0.5)
                alert("Vous avez gagné!")
                init(largeur, hauteur)
        

        
# La variable style contient le texte qui formate le style de la grille de jeu.

style= '''<style>
     #main table {
        border: 1px solid black;
        margin: 10px;
      }
     
     #main table td {
        width: 30px;
        height: 30px;
        border: none;}
     
     .bouton {
     overflow:auto;
        display: inline-block;
        margin:0;
        padding:0;
        width: 100%;
        height: 100%
      }  
      
      </style>'''


main = document.querySelector('#main')
main.innerHTML = '''
<link rel="preload" href="http://codeboot.org/images/minesweeper/0.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/1.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/2.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/3.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/4.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/5.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/6.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/7.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/8.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/blank.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/flag.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/mine.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/mine-red.png">
<link rel="preload" href="http://codeboot.org/images/minesweeper/
mine-red-x.png">'''







# La procédure init prend en paramètre deux entiers positifs qui représentent 
# le nombre de cases de largeur et de hauteur pour faire la grille de jeu. Elle
# démarre le jeu en mettant le bon nombre de tuiles non dévoilées.

def init(largeur, hauteur):
    global  grilleAfficher
    
  
    #créer la grille qui contient seulement des blank et sera dévoilée 
    #progressivement
    grilleAfficher = creerGrille(largeur, hauteur)

 
    #modifier l'élément main pour y mettre la grille de jeu
    main.innerHTML = style + tab2Html(grilleAfficher, largeur, hauteur)
    

init(8,5)


####  Tests unitaires  ####


#La fonction testDemineur teste les fonctions de demineur.py et arrête le
#programme si l'un des test ne renvoie pas le résultat attendu

def testDemineur():
    global grilleAfficher, grilleChiffres
    
    ###Test de la fonction image
    #test de la fonction image pour 0
    assert image(0)=='<img src="http://codeboot.org/images/minesweeper/0.png">'
    
    #test de la fonction image pour 8
    assert image(8)=='<img src="http://codeboot.org/images/minesweeper/8.png">'
    
    
    ###Test de la fonction creerGrille
    #test de la fonction pour une grille de taille 1*2
    assert creerGrille(1,2) == [
        '<img src="http://codeboot.org/images/minesweeper/blank.png">',
        '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    #test de la fonction pour une grille de taille 0*0
    assert creerGrille(0,0) == []
    
    
    ###Test de la fonction trouverCasesAutour
    grille = ['<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    #test de la fonction pour une case dans un coin de la grille
    assert trouverCasesAutour(grille, 3, 3, 0) == [1, 4, 3]
    
    #test de la fonction pour une case au milieu de la grille
    assert trouverCasesAutour(grille, 3, 3, 4) == [5, 8, 7, 6, 3, 0, 1, 2]
    
    
    ###Test de la fonction compterMines
    #test de la fonction pour deux mines dans la grille
    grille = ['<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">']
    
    assert compterMines(grille, 3, 3) == [
        '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/1.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/2.png">',
              '<img src="http://codeboot.org/images/minesweeper/2.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/1.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">']
    
    
    #test de la fonction pour aucune mine dans la grille
    grille = ['<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">']
    
    assert  compterMines(grille, 3, 3) == [
        '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">']
    
    
    ###Test de la fonction tab2Html
    grille = ['<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    assert tab2Html(grille, 3,3) == '<table><tr><td id="case0"  ' + \
    'onclick= "clic(0, event.shiftKey,3,3)">'''+ \
    '<img src="http://codeboot.org/images/minesweeper/blank.png">'+\
    '</td><td id="case1"  onclick= "clic(1, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png">'+\
    '</td><td id="case2"  onclick= "clic(2, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png">'+\
    '</td></tr><tr><td id="case3"  onclick= "clic(3, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png"></td>'+\
    '<td id="case4"  onclick= "clic(4, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png"></td>'+\
    '<td id="case5"  onclick= "clic(5, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png"></td></tr>'+\
    '<tr><td id="case6"  onclick= "clic(6, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png"></td>'+\
    '<td id="case7"  onclick= "clic(7, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png"></td>'+\
    '<td id="case8"  onclick= "clic(8, event.shiftKey,3,3)">'+\
    '<img src="http://codeboot.org/images/minesweeper/blank.png">'+\
    '</td></tr></table>'
    
    ###Test de la fonction devoiler
    #test de la fonction pour une grilleChiffres remplie de 0
    grilleAfficher = [
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    grilleChiffres = [
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">']
    
    assert devoiler(1, 3, 3) == [
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">']
    
    
    #test de la fonction pour une grille chiffre avec 8 mines pour 9 cases
    grilleAfficher = [
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    grilleChiffres = [
              '<img src="http://codeboot.org/images/minesweeper/3.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">']
    
    assert devoiler(0, 3, 3) == [
              '<img src="http://codeboot.org/images/minesweeper/3.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    
    #test de la fonction pour afficher les cases vides adjacentes et les
    #cases chiffres accolées aux cases vides
    grilleAfficher = [
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
    
    grilleChiffres = [
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/1.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/2.png">',
              '<img src="http://codeboot.org/images/minesweeper/2.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/1.png">',
              '<img src="http://codeboot.org/images/minesweeper/mine.png">']
    
    assert devoiler(0, 3, 3) == [
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/1.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/2.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">',
              '<img src="http://codeboot.org/images/minesweeper/0.png">',
              '<img src="http://codeboot.org/images/minesweeper/1.png">',
              '<img src="http://codeboot.org/images/minesweeper/blank.png">']
