import pygame, sys, random
from pygame.locals import *

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
s=pygame.display.set_mode((224,288))
pygame.display.set_caption('PacMan')
clock=pygame.time.Clock()
sp=pygame.image.load('graphics\spritetrans.png')

vol=1
pygame.mixer.music.load('sounds\pacman_beginning.wav')
pygame.mixer.music.set_volume(vol)
pygame.time.delay(200)
pygame.mixer.music.play()
chomp1=pygame.mixer.Sound('sounds\pacman_chomp1.wav')
chomp1.set_volume(vol)
chomp2=pygame.mixer.Sound('sounds\pacman_chomp2.wav')
chomp2.set_volume(vol)

##########VARIABLES##########

b=0
c=2
chompt=0
d=2
dot=0
full=0
fps=60
g=[(112+1,116),(112,140-0.5),(96,140+0.5),(128,140+0.5)]
gd=[2,1,0,0]
gdot=[0,0,30,60]
gfright=0
gmode=[1,4,4,4]#0Chase  1Scatter  2Fright  3Death  4House  5Spawn  6Despawn
gmodemain=1
gmodet=[999999,84,79,59,54,34,27,7]
gswitch=[0,0,0,0]
gt=0
gtf=0
m=[]
p=(112+1,211)
pm=(0,0)
pt=0
rdy=0
sc=0

for l in open('map.txt').readlines():
	l=list(l)
	l.pop()
	m.append(l)

####################START OF MAIN LOOP####################
	
while True:

	##########PACMAN##########

	#Input
	for e in pygame.event.get():
		if e.type==QUIT:sys.exit()
		elif e.type==KEYDOWN:
			if e.key==K_UP:c=0
			elif e.key==K_DOWN:c=1
			elif e.key==K_LEFT:c=2
			elif e.key==K_RIGHT:c=3
			
	#Edibles
	pm=(int((p[0]-p[0]%8)/8),int((p[1]-p[1]%8)/8))		
	if p[0]%8==4 and p[1]%8==3:
		if m[pm[1]][pm[0]]=='.':
			m[pm[1]][pm[0]]=' '
			sc+=10
			dot+=1
			if chompt==0:
				chomp1.play()
				chompt=1
			else:
				chomp2.play()
				chompt=0
		elif m[pm[1]][pm[0]]=='o':
			m[pm[1]][pm[0]]=' '
			sc+=50
			dot+=1
			if chompt==0:
				chomp1.play()
				chompt=1
			else:
				chomp2.play()
				chompt=0
			gfright=1
			gtf=0
			for n in range(0,4):
				if gmode[n]<=2:
					gmode[n]=2
					gswitch[n]=1
		
	#Change Direction & Collusion Detection
		if pm[0]==0 or pm[0]==27 or pm[1]==0 or pm[1]==35:pass
		else:
			if d==0 and m[pm[1]-1][pm[0]]=='X' or d==1 and m[pm[1]+1][pm[0]]=='X' or d==2 and m[pm[1]][pm[0]-1]=='X' or d==3 and m[pm[1]][pm[0]+1]=='X':b=1
			if c==0 and m[pm[1]-1][pm[0]]=='X' or c==1 and m[pm[1]+1][pm[0]]=='X' or c==2 and m[pm[1]][pm[0]-1]=='X' or c==3 and m[pm[1]][pm[0]+1]=='X':pass
			else:d=c
	if d==0 and c==1 or d==1 and c==0 or d==2 and c==3 or d==3 and c==2:d=c
	
	#Movement
	if b==0:
		if d==0:p=(p[0],p[1]-1)
		elif d==1:p=(p[0],p[1]+1)
		elif d==2:p=(p[0]-1,p[1])
		else:p=(p[0]+1,p[1])
		if p[0]==-1:p=(224,p[1])
		elif p[0]==225:p=(0,p[1])
		if p[1]==-1:p=(p[0],288)
		elif p[1]==289:p=(p[0],0)
		pt+=1
	else:b=0
	
	##########GHOSTS##########
	
	#Targeting
	gtar=[]
	for n in range(0,4):
		
		#0Chase
		if gmode[n]==0:
			if n==0:gtar=[pm]
			elif n==1:
				if d==0:gtar.append((pm[0],pm[1]-4))
				elif d==1:gtar.append((pm[0],pm[1]+4))
				elif d==2:gtar.append((pm[0]-4,pm[1]))
				else:gtar.append((pm[0]+4,pm[1]))
			elif n==2:
				gm=(int((g[0][0]-g[0][0]%8)/8),int((g[0][1]-g[0][1]%8)/8))	
				if d==0:gtar.append((pm[0]*2-gm[0],(pm[1]-2)*2-gm[1]))
				elif d==1:gtar.append((pm[0]*2-gm[0],(pm[1]+2)*2-gm[1]))
				elif d==2:gtar.append(((pm[0]-2)*2-gm[0],pm[1]*2-gm[1]))
				else:gtar.append(((pm[0]+2)*2-gm[0],pm[1]*2-gm[1]))
			elif n==3:
				gm=(int((g[3][0]-g[3][0]%8)/8),int((g[3][1]-g[3][1]%8)/8))
				if (gm[0]-pm[0])**2+(gm[1]-pm[1])**2<=64:gtar.append((0,35))
				else:gtar.append(pm)
			if gt/fps<999999:
				if gmodet.count(gt/fps)==1:
					gmode[n]=1
					gmodemain=1
					gswitch[n]=1
		
		#1Scatter
		elif gmode[n]==1:
			tarset=[(27,0),(0,0),(27,35),(0,35)]
			gtar.append(tarset[n])
			if gt/fps<999999:
				if gmodet.count(gt/fps)==1:
					gmode[n]=0
					gmodemain=0
					gswitch[n]=1
					
		#2Fright
		elif gmode[n]==2:
			gtar.append((random.randint(0,27),random.randint(0,36)))
			if gtf/fps==6:
				gmode[n]=gmodemain
				gfright=0
				
		#Change Direction & Collusion Detection
		if gmode[n]<=3:
			if gswitch[n]==0:
				gm=(int((g[n][0]-g[n][0]%8)/8),int((g[n][1]-g[n][1]%8)/8))	
				if g[n][0]%8==4 and g[n][1]%8==4 and gm[0]!=0 and gm[0]!=27 and gm[1]!=0 and gm[1]!=35:
					dirset=[0,1,2,3]
					if gd[n]==1 or m[gm[1]-1][gm[0]]=='X':dirset.remove(0)
					if gd[n]==0 or m[gm[1]+1][gm[0]]=='X':dirset.remove(1)
					if gd[n]==3 or m[gm[1]][gm[0]-1]=='X':dirset.remove(2)
					if gd[n]==2 or m[gm[1]][gm[0]+1]=='X':dirset.remove(3)
					posset=[(gm[0],gm[1]-1),(gm[0],gm[1]+1),(gm[0]-1,gm[1]),(gm[0]+1,gm[1])]
					while len(dirset)!=1:
						if (posset[dirset[0]][0]-gtar[n][0])**2+(posset[dirset[0]][1]-gtar[n][1])**2>(posset[dirset[1]][0]-gtar[n][0])**2+(posset[dirset[1]][1]-gtar[n][1])**2:dirset.remove(dirset[0])
						else:dirset.remove(dirset[1])
					gd[n]=dirset[0]
			else:
				gswitch[n]=0
				if gd[n]==0:gd[n]=1
				elif gd[n]==1:gd[n]=0
				elif gd[n]==2:gd[n]=3
				else:gd[n]=2
		
			#Movement
			if gd[n]==0:g[n]=(g[n][0],g[n][1]-1)
			elif gd[n]==1:g[n]=(g[n][0],g[n][1]+1)
			elif gd[n]==2:g[n]=(g[n][0]-1,g[n][1])
			else:g[n]=(g[n][0]+1,g[n][1])
			if g[n][0]==-1:g[n]=(224,g[n][1])
			elif g[n][0]==225:g[n]=(0,g[n][1])
			if g[n][1]==-1:g[n]=(g[n][0],288)
			elif g[n][1]==289:g[n]=(g[n][0],0)
		
		#4House
		elif gmode[n]==4:
			if gdot[n]<=dot:
				gmode[n]=5
			if g[n][1]<=136:gd[n]=1
			elif g[n][1]>=144:gd[n]=0
			if gd[n]==0:g[n]=(g[n][0],g[n][1]-0.5)
			elif gd[n]==1:g[n]=(g[n][0],g[n][1]+0.5)
		
		#5Spawn
		elif gmode[n]==5:
			if g[n][0]<112:
				gd[n]=3
				g[n]=(g[n][0]+0.25,g[n][1])
			elif g[n][0]>112:
				gd[n]=2
				g[n]=(g[n][0]-0.25,g[n][1])
			elif g[n][1]>116:
				gd[n]=0
				g[n]=(g[n][0],g[n][1]-0.25)
			else:
				gmode[n]=gmodemain
				gd[n]=2
	
	##########GRAPHICS##########
	
	#Score
	s.blit(sp,(0,0),(100,0,224,288))
	scl=list(str(sc))
	for n in range(0,len(scl)):
		s.blit(sp,(56-8*(len(scl)-n),8),(8*int(scl[n]),280,8,8))
	
	#Edibles
	for y in range(0,len(m)):
		for x in range(0,len(m[y])):
			if m[y][x]=='.':s.blit(sp,(8*x+3,8*y+3),(0,13,2,2))
			elif m[y][x]=='o':s.blit(sp,(8*x,8*y),(0,15,8,8))
			
	#Pacman
	if pt%8==0 or pt%8==1:s.blit(sp,(p[0]-6,p[1]-6),(0,0,13,13))
	elif pt%8==4 or pt%8==5:s.blit(sp,(p[0]-6,p[1]-6),((d+1)*13,13,13,13))
	else:s.blit(sp,(p[0]-6,p[1]-6),((d+1)*13,0,13,13))
	
	#Ghosts
	for n in range(0,4):
		if gfright==1:
			if gtf%16<=7:s.blit(sp,(int(g[n][0]-7),int(g[n][1]-7)),(0,152,14,14))
			else:s.blit(sp,(int(g[n][0]-7),int(g[n][1]-7)),(0,166,14,14))
		else:
			if gt%16<=7:s.blit(sp,(int(g[n][0]-7),int(g[n][1]-7)),((gd[n])*14,n*28+40,14,14))
			else:s.blit(sp,(int(g[n][0]-7),int(g[n][1]-7)),((gd[n])*14,n*28+26,14,14))
	if gfright==1:gtf+=1
	else:gt+=1
	
	pygame.display.update()
	
	#Ready
	if rdy==0:
		s.blit(sp,(89,160),(0,273,46,7))
		pygame.display.update()
		pygame.time.delay(4500)
		pygame.mixer.music.load('sounds\pacman_siren.wav')
		pygame.mixer.music.set_volume(vol)
		pygame.mixer.music.play(-1)
		rdy=1
		
	clock.tick(60)
