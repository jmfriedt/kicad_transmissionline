#!/usr/bin/env python

import pcbnew 
import math 
dL=2000000	# spacing between vias
R=2000000	# distance to track
pcb = pcbnew.GetBoard()

nets = pcb.GetNetsByName()
gndnet = nets.find("GND").value()[1]
gndclass = gndnet.GetNetClass()
print(str(gndnet.GetNetname())+" "+str(gndnet.GetNet()))

gndcode=gndnet.GetNet();

for track in pcb.GetTracks():
	start = track.GetStart()
	end = track.GetEnd()
#	print(track.GetNetCode())
#	if track.GetNetCode()==0 :
	if track.IsSelected():
		n=math.floor(track.GetLength()/dL)
		m=0
		if ((track.GetEnd().x-track.GetStart().x) != 0):
			a=(track.GetEnd().y-track.GetStart().y)/(track.GetEnd().x-track.GetStart().x)
			b=track.GetStart().y-a*track.GetStart().x
			theta=math.atan(a)
			print(str(theta))
#			for x in range(track.GetStart().x,track.GetEnd().x,int(dL*math.cos(theta))):
			x=min(track.GetStart().x,track.GetEnd().x)
			while x<max(track.GetStart().x,track.GetEnd().x):
				yp=a*x+b+R*math.sin(theta+3.14159/2)
				xp=x+R*math.cos(theta+3.14159/2)
				newvia=pcbnew.VIA(pcb)
				newvia.SetLayerPair(pcbnew.PCBNEW_LAYER_ID_START, pcbnew.PCBNEW_LAYER_ID_START+31)
				newvia.SetPosition(pcbnew.wxPoint(xp,yp))
				newvia.SetViaType(pcbnew.VIA_THROUGH)
				newvia.SetWidth(1000000)
				newvia.SetNetCode(gndcode)
				pcb.Add(newvia)
				yp=a*x+b+R*math.sin(theta-3.14159/2)
				xp=x+R*math.cos(theta-3.14159/2)
				newvia=pcbnew.VIA(pcb)
				newvia.SetLayerPair(pcbnew.PCBNEW_LAYER_ID_START, pcbnew.PCBNEW_LAYER_ID_START+31)
				newvia.SetPosition(pcbnew.wxPoint(xp,yp))
				newvia.SetViaType(pcbnew.VIA_THROUGH)
				newvia.SetWidth(1000000)
				newvia.SetNetCode(gndcode)
				pcb.Add(newvia)
				x=x+dL*math.cos(theta)
		elif track.GetLength()>0:
			x=track.GetStart().x
			print("Vertical: Start: "+str(track.GetStart().y)+" End: "+str(track.GetEnd().y))
			y=min(track.GetStart().y,track.GetEnd().y)
			while y<max(track.GetStart().y,track.GetEnd().y):
				xp=x+R
				newvia=pcbnew.VIA(pcb)
				newvia.SetLayerPair(pcbnew.PCBNEW_LAYER_ID_START, pcbnew.PCBNEW_LAYER_ID_START+31)
				newvia.SetPosition(pcbnew.wxPoint(xp,y))
				newvia.SetViaType(pcbnew.VIA_THROUGH)
				newvia.SetWidth(1000000)
				newvia.SetNetCode(gndcode)
				pcb.Add(newvia)
				xp=x-R
				newvia=pcbnew.VIA(pcb)
				newvia.SetLayerPair(pcbnew.PCBNEW_LAYER_ID_START, pcbnew.PCBNEW_LAYER_ID_START+31)
				newvia.SetPosition(pcbnew.wxPoint(xp,y))
				newvia.SetViaType(pcbnew.VIA_THROUGH)
				newvia.SetWidth(1000000)
				newvia.SetNetCode(gndcode)
				pcb.Add(newvia)
				y=y+dL
pcbnew.Refresh()
