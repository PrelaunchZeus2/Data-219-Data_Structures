"""
A Tkinter.Canvas derived class with some
helpful things for drawing and updating...
"""

import random
from tkinter import *
import math

class Affine2dTrans:
    """ let's create our own 2d affine class """

    def __init__(self):
        """ the components currently supported """ 
        self.scalex = 1.0  # units of  pixels per worldunit (cm)
        self.scaley = 1.0  # units of  pixels per worldunit (cm)
        self.cx = 0.0      # worldunits (cm)
        self.cy = 0.0      # worldunits (cm)
        self.px = 0.0      # pixels
        self.py = 0.0      # pixels
        self.thr = 0.0     # radians, though the interface is always degrees
        self.sinthr = math.sin(0.0)   # why compute this more than once?
        self.costhr = math.cos(0.0)   # why not say it more than once?

    def transform(self, xy):
        return self.transformWorldToPixel(xy)

    def transformWorldToPixel(self, world):
        """ outpus pixel coordinates for the input world coords """
        # first, compute the offset from the world's center of rotation
        offx = world[0] - self.cx
        offy = world[1] - self.cy
        # next, rotate the resulting vector by theta
        rx = self.costhr * offx - self.sinthr * offy
        ry = self.sinthr * offx + self.costhr * offy
        # next, scale the result
        rx = rx * self.scalex
        ry = ry * self.scaley
        # finally, add the pixel offset
        return ( self.px + rx, self.py + ry )

    def transformPixelToWorld(self, pixel):
        """ outputs world coordinates for the input pixel coords """
        # first subtract the pixel offset
        rx = pixel[0] - float(self.px)
        ry = pixel[1] - float(self.py)
        # unscale the result
        rx = rx / self.scalex
        ry = ry / self.scaley
        # unrotate the vector by theta
        offx =  self.costhr * rx + self.sinthr * ry
        offy = -self.sinthr * rx + self.costhr * ry
        # add the world offset to get world coords
        return (offx + self.cx, offy + self.cy)

    def transform_scale(self, length, thd):
        """ returns the new length equivalent in pixels to  the input
            length along the thd direction (in degrees) - if x and y
            are not equal, thd will make a difference... 

            length sould be positive - a positive result will be
            returned in any case

            thd is in global world terms, not relative to the
            stored thr within this transformation """
        # first, compute the offset from the world's center of rotation
        thr = thd * 180.0 / math.pi
        offx = length * math.cos(thr)
        offy = length * math.sin(thr)
        # next, scale the result
        rx = offx * self.scalex
        ry = offy * self.scaley
        # finally, compute the magnitude
        return ( math.sqrt( rx * rx + ry * ry ) )
        
    def deltaWorldRotationCenter(self, deltaworldx, deltaworldy):
        """ moves the world rotation center by the amounts
            provided in the inputs deltaworldx and deltaworldy
        """
        self.cx += deltaworldx
        self.cy += deltaworldy

    def setWorldRotationCenter(self, worldcenterx, worldcentery):
        """ puts the input world point onto the input pixel point
            and make that point the center of any rotation specified """
        # I don't know if rotation should be preserved through this call...
        self.cx = worldcenterx
        self.cy = worldcentery

    def setPixelRotationCenter(self, pixelx, pixely):
        """ puts the input world point onto the input pixel point
            and make that point the center of any rotation specified 
        """
        # I don't know if rotation should be preserved through this call...
        self.px = pixelx
        self.py = pixely

    def setScales(self, scale_x, scale_y):
        """ allows for axis flipping and nonuniform (!) scaling, though
            why you'd want that is beyond me... each of scale_x and 
            scale_y are expressed in pixels per world unit (cm) "
        """
        if scale_x == 0.0 or scale_y == 0.0:
            print("Warning - you don't want a finite world length mapping to 0 pixels!")
        self.scalex = scale_x
        self.scaley = scale_y
    
    def setScalesAbsVal(self, scale_x, scale_y):
        """ this will preserve the signs of self.scalex and self.scaley,
            setting their absolute values to scale_x and scale_y, respectively
        """
        if scale_x == 0.0 or scale_y == 0.0:
            print("Warning - you don't want a finite world length mapping to 0 pixels!")
        if self.scalex > 0: self.scalex = abs(scale_x)
        else:               self.scalex = -abs(scale_x)
        if self.scaley > 0: self.scaley = abs(scale_y)
        else:               self.scaley = -abs(scale_y)

    def multiplyScales(self, mult_x, mult_y):
        """ change the x and y scales by multiplying by the inputs 
            scalex and scaley are in units of pixels per world unit (cm)
        """
        if mult_x == 0.0 or mult_y == 0.0:
            print("Warning - you don't want a finite world length mapping to 0 pixels!")
        self.scalex *= mult_x
        self.scaley *= mult_y

    def setRotationAngle(self, thd):
        """ set the number of degrees which the world coordinates
            are rotated (around the rotation center) before mapping to pixels """
        self.thr = thd * math.pi / 180.0
        self.costhr = math.cos(self.thr)
        self.sinthr = math.sin(self.thr)

    def deltaRotationAngle(self, thd):
        """ changes the number of degrees which the world coordinates
            are rotated (around the rotation center) before mapping to pixels """
        self.thr = self.thr + (thd * math.pi / 180.0)
        self.costhr = math.cos(self.thr)
        self.sinthr = math.sin(self.thr)



class Movable:
    """ Movable is a wrapper around Tkinter.Canvas objects
        it holds their _global_ coordinates, converting to
        pixel coordinates as necessary (saving time, perhaps...)

        It can be subclassed to allow for all sorts of
        composite objects to be treated as one, with their
        own, object-local coordinate system
    """

    def __init__(self, canvas, cx=0.0, cy=0.0, thr=0.0, colorstr='black'):
        """ set up a local coordinate system """
        self.canvas = canvas
        # self.tag = 'notag'  # don't seem to be using this...
        self.cx = cx
        self.cy = cy
        self.thr = thr
        self.colorstr = colorstr
        self.sinthr = math.sin(self.thr)
        self.costhr = math.cos(self.thr)
        self.localCoords = []
        self.updateGlobalCoords() # sets self.globalCoords
        self.canvas.addMovable(self) # adds self object to the canvas's list

    def localToGlobalCoords(self, xy):
        """ transforms one point from object-local to global
            coordinates

            self.cx and self.cy are the global location of the 
            center of the object-local coordinate system, and it's
            facing self.thr
        """
        return ( (xy[0]*self.costhr - xy[1]*self.sinthr + self.cx, 
                  xy[0]*self.sinthr + xy[1]*self.costhr + self.cy) )

    def updateGlobalCoords(self):
        """ create global coordinates if the object-local coordinates
            are centered at (cx,cy) facing thr
            input L: should be a list of tuples

            could be overridden
        """
        self.globalCoords = [ self.localToGlobalCoords(T) for T in self.localCoords ]
        #print 'cx,cy,thd are', self.cx, self.cy, math.degrees(self.thr)
        #print 'globalCoords are', self.globalCoords

    def deltaGlobalPose( self, dx, dy, dthr ):
        """ change the global pose of this object """
        self.setGlobalPose( self.cx+dx, self.cy+dy, self.thr+dthr )

    def setGlobalPose( self, cx, cy, thr ):
        """ set the absolute global pose of this object """
        self.cx = cx
        self.cy = cy
        self.thr = thr
        self.sinthr = math.sin(self.thr)
        self.costhr = math.cos(self.thr)
        self.updateGlobalCoords()
        self.updatePixelCoords()

    def setColor( self, r, g, b ):
        """ this writes the appropriate color string """
        self.colorstr = "#%02x%02x%02x" % (r,g,b)
        self.canvas.itemconfigure( self.itemid, fill=colorstr )

    def setColorstr( self, colorstr ):
        """ this takes a color name """
        self.colorstr = colorstr
        self.canvas.itemconfigure( self.itemid, fill=colorstr )

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
            should be overridden
        """
        print('in Movable\'s updatePixelCoords')

    def createObjects( self ):
        """ computes pixel coordinates and then creates the canvas objects
            should be overridden
        """
        print('in Movable\'s createObjects')
        
    def delete( self ):
        """ deletes the items from the canvas
        """
        # should be the list of items!
        # some have more than 1!
        self.canvas.delete( self.itemid )

        
        
       
class MovablePixelLengthLine(Movable):
    
    def __init__(self, canvas, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black', width=2, pixellength=8, arrow=None):
        """ the MovablePixelLengthLine constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.width = width
        self.pixellength = pixellength
        self.arrow = arrow
        self.localCoords = [ (0.0,0.0),    # these are object-local coordinates
                             (1.0,0.0) ]   # except the length is wrong...
        self.updateGlobalCoords()        # now in world coords, (cx,cy)
        self.createObjects()             # using self.pixellength
        
    def changeAnchor( self, cx, cy, thr=None ):
        """ changeAnchor moves the starting point of the line, cx, and cy,
            both in world coordinates. thr is optional and will reorient the
            line from its anchor for its designated pixel length
        """
        # can't use   if not thr  below because thr might be 0.0 !!
        if thr == None:
            thr = self.thr
        self.setGlobalPose( cx, cy, thr )
        #print 'global pose set to', cx, cy, math.degrees(thr), 'in changeAnchor'
        self.updatePixelCoords()
        
    def computeEndVertex( self, p ):
        """ returns a tuple with the pixel coordinates of the end vertex
            if the initial vertex has pixel coordinates of p[0][0], p[0][1]
            and the end vertex is currently p[1][0], p[1][1] (the wrong length)
        """
        #print 'p is', p
        length = math.sqrt( (p[1][0] - p[0][0])**2 + (p[1][1] - p[0][1])**2 )
        ratio = self.pixellength / float(length)
        #print 'l and ratio are', length, ratio
        endx = p[0][0] + (p[1][0]-p[0][0])*ratio
        endy = p[0][1] + (p[1][1]-p[0][1])*ratio
        #print 'endx,y are', endx, endy
        return endx, endy
        

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # p has the pixel coords of the anchor (starting vertex)
        p = map( self.canvas.tfm.transform, self.globalCoords )
        # now we need to find the other endpoint by scaling p[1] and p[2]
        # so that the length of their sum is self.;pixellength
        endx, endy = self.computeEndVertex(p)
        self.canvas.coords( self.itemid, p[0][0], p[0][1], 
                                         endx, endy )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        endx, endy = self.computeEndVertex(p)
        self.itemid = self.canvas.create_line(p[0][0], p[0][1], 
                                              endx,    endy,
                                              fill=self.colorstr,
                                              width=self.width) 
        if self.arrow:
            self.canvas.itemconfigure( self.itemid, arrow='last',
                                                    capstyle='round' )
        
        
        
        
class MovablePoint(Movable):

    def __init__(self, canvas, cx=0.0, cy=0.0, 
                       colorstr='black', pixelradius=2):
        """ the MovablePoint constructor """
        Movable.__init__(self, canvas, cx, cy, 0.0, colorstr)
        self.pixelradius = int(pixelradius)
        self.localCoords = [ (0,0) ]
        self.updateGlobalCoords()
        self.createObjects()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.pixelradius
        self.canvas.coords( self.itemid, p[0][0]-r, p[0][1]-r, 
                                         p[0][0]+r, p[0][1]+r )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.pixelradius
        self.itemid = self.canvas.create_oval(p[0][0]-r, p[0][1]-r, 
                                              p[0][0]+r, p[0][1]+r,
                                              fill=self.colorstr, 
                                              outline='')
        
        
        
        
class MovableCircle(Movable):

    def __init__(self, canvas, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black', radius=10.0):
        """ the MovableCircle constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.radius = radius
        self.localCoords = [ (0.0,0.0), (self.radius,0.0) ]
        self.updateGlobalCoords()
        self.createObjects()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.canvas.tfm.transform_scale( self.radius, 0.0 )
        self.canvas.coords( self.itemid, p[0][0]-r, p[0][1]-r, 
                                         p[0][0]+r, p[0][1]+r )
        self.canvas.coords( self.itemid2, p[0][0],p[0][1],
                                          p[1][0],p[1][1])

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.canvas.tfm.transform_scale( self.radius, 0.0 )
        self.itemid = self.canvas.create_oval(p[0][0]-r, p[0][1]-r, 
                                              p[0][0]+r, p[0][1]+r,
                                              fill=self.colorstr, 
                                              outline='black')
        self.itemid2 = self.canvas.create_line(p[0][0],p[0][1],
                                               p[1][0],p[1][1],
                                               fill='white',width=2)
                                               


class MovableLine(Movable):

    def __init__(self, canvas, endpoints, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black', width=2):
        """ the MovableLine constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.width = width
        self.localCoords = endpoints[:]  # should be two 2-tuples
        self.updateGlobalCoords()
        self.createObjects()
        
    def changeCoords( self, newcoords ):
        """ should be called updateWorldCoords!
        """
        # remember this "localCoords" is object-local (NOT pixel)
        self.localCoords = newcoords[:]  # better be the right format!
        self.updateGlobalCoords()
        self.updatePixelCoords()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.canvas.coords( self.itemid, p[0][0], p[0][1], 
                                         p[1][0], p[1][1] )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.itemid = self.canvas.create_line(p[0][0], p[0][1], 
                                              p[1][0], p[1][1],
                                              fill=self.colorstr,
                                              width=self.width) 


class MovableRect(Movable):

    def __init__(self, canvas, tlbr_endpoints, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black'):
        """ the MovableRect constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        [ (tlx,tly), (brx,bry) ] = tlbr_endpoints
        # need to use a polygon so we can rotate...
        self.localCoords = [ (tlx,tly), (tlx,bry), (brx,bry), (brx,tly) ]
        self.updateGlobalCoords()
        self.createObjects()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = list(map( self.canvas.tfm.transform, self.globalCoords ))
        self.canvas.coords( self.itemid, p[0][0], p[0][1], 
                                         p[1][0], p[1][1],
                                         p[2][0], p[2][1],
                                         p[3][0], p[3][1] )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = list(map( self.canvas.tfm.transform, self.globalCoords ))
        self.itemid = self.canvas.create_polygon(p[0][0], p[0][1], 
                                                 p[1][0], p[1][1],
                                                 p[2][0], p[2][1],
                                                 p[3][0], p[3][1],
                                                 fill=self.colorstr,
                                                 outline="black") 
class MovablePoly(Movable):

    def __init__(self, canvas, path_endpoints, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black'):
        """ the MovablePoly constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.localCoords = path_endpoints[:]
        self.colorstr = colorstr
        self.updateGlobalCoords()
        self.createObjects()
        
    def mappend(self,f,pointlist):
        """ just like mappend in CS 60
        """
        if len(pointlist) == 0: return []
        fp = f(pointlist[0])
        return [fp[0],fp[1]] + self.mappend(f,pointlist[1:])
        

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        #p = map( self.canvas.tfm.transform, self.globalCoords 
        p = self.mappend( self.canvas.tfm.transform, self.globalCoords )
        #print 'p is', p
        # seems to want integral pixel values... fair enough
        p = map(int,p)
        #print 'now p is', p
        # it seems that the following call wants p in a flattened list
        # instead of a list of pairs
        self.canvas.coords( self.itemid, tuple(p) )
        # HERE for poly

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.itemid = self.canvas.create_polygon(p,
                                                 fill=self.colorstr,
                                                 outline=self.colorstr)
                          # it's good to have the outline be the same color
                          # to minimize gaps...


class ErdosCanvas(Canvas):
    """ This is a dervied class from canvas with support for
        a global transformation (tfm) and multiple objects
    """

    def __init__(self,master,height=400,width=400):
        """ a canvas to show a robot running around and a map
            a key facility is a general transformation allowing
            a user to specify everything in global coordinates
            and leave all of the translation to pixel coordinates
            to the computer (good!)
        """
        Canvas.__init__(self,master)
        # basic data members 
        self.master = master
        self.height = height   # window height
        self.width  = width    # window width
        self.scrollWidth = width
        self.scrollHeight = height  # this we'll work on later...

        # here is the transformation...
        self.tfm = Affine2dTrans()
        self.tfm.setWorldRotationCenter(0,0) # maps the world point 0,0 to 
        self.tfm.setPixelRotationCenter(self.width/2,self.height/2) # the center of the window

        # things in the world...
        self.movables = []   # for possibly moving objects with local coords

        # dictionary for keys pressed
        self.keysdown = {}

        self.configure(bg='white', width=self.width, height=self.height)
        self.bind("<Configure>", self.configcallback)

        # this will bring the focus to the main canvas...
        self.focus_set()
        self.bind("<KeyPress>", self.keypresscallback)
        self.bind("<KeyRelease>", self.keyreleasecallback)
        self.configure(highlightthickness=0)

        # handle all of the button events...
        self.bind("<Button-1>", self.b1_down)
        self.bind("<B1-Motion>", self.b1_move)
        self.bind("<ButtonRelease-1>", self.b1_up)

        self.bind("<Button-2>", self.click_b2_down)
        self.bind("<B2-Motion>", self.click_b2_move)
        self.bind("<ButtonRelease-2>", self.click_b2_up)

        self.bind("<Button-3>", self.click_b3_down)
        self.bind("<B3-Motion>", self.click_b3_move)
        self.bind("<ButtonRelease-3>", self.click_b3_up)

    # end of the __init__ constructor

    def reconfig(self):
        """ check h and w... """
        h = int(self.cget('height'))
        w = int(self.cget('width'))
        #print 'h,w are', h, w
        self.width = w
        self.height = h
        self.tfm.setPixelRotationCenter(self.width/2,self.height/2) 
        self.redraw()

    def configcallback(self, event):
        """ configcallback handles resizing, etc. """
        #print "***** config! *****"
        #print "dir is", dir(event)
        #print 'char, delta, height, keycode are', event.char, event.delta, event.height, event.keycode
        #print 'keysym, keysym_num, num, send_event', event.keysym, event.keysym_num, event.num, event.send_event
        #print 'serial, state, time, type', event.serial, event.state, event.time, event.type
        #print 'widget, width, x, x_root, y, y_root', event.widget, event.width, event.x, event.x_root, event.y, event.y_root
        #print "***** ******* *****"
        self.height = event.height 
        self.width = event.width
        # print 'h,w are', self.height, self.width
        # so that the world rotation center maps to the center of the window...
        self.tfm.setPixelRotationCenter(self.width/2,self.height/2) 
        self.startx = self.width/2    # for GUI events that change tfm
        self.starty = self.height/2
        self.redraw()
    
    def keypresscallback(self, event):
        """ handling keypresses """
        c = event.char
        #print 'keysym is', event.keysym
        #print 'c is', c

        # add an entry to our keysdown dictionary
        self.keysdown[event.keysym] = 1

        if c == '?':
            # way to ask about things on the fly!
            #print 'dir is', dir(tkv.canvas)
            #print 'help is', help(tkv.canvas.create_polygon)
            print('\n\
csplot Help \n\
  Controls \n\
    shift+mousedrag:  zooms in/out as you go towards/away from the center \n\
    x+mousedrag:     zooms only the horizontal axis \n\
    y+mousedrag:     zooms only the vertical axis \n\
    z+mousedrag:     zooms in on the box defined by the cursor \n\
    t+mousedrag:     translates (slides) the canvas around \n\
    ctrl+left click: centers the view at the clicked position \n\
    p+left click:    prints the coordinates of the mouse pointer \n\
    R:               resets the zoom and centers the view\n\
    ?:               displays csplot Help')

        # char is the empty string for special (non-char) keys
        #print 'keysym is', event.keysym # things like 'Shift_R' for right shift key, etc.

        #reset the zoom
        if c == 'R':
            w = _getwin()
            w.canv.tfm.setScales(50,-50)
            w.canv.tfm.setWorldRotationCenter(0,0)
            w.canv.tfm.setPixelRotationCenter(w.canv.width/2, w.canv.height/2)
            self.redraw()

    def keyreleasecallback(self, event):
        """ handling keyreleases """
        k = event.keysym
        #print "key RELEASE of", k
        if event.keysym in self.keysdown:
            self.keysdown[event.keysym] = 0

    def loadMap(self, filename):
        """ loadMap reads in a file of obstacles and places them
            on this (self) canvas
        """
        # first clear the old stuff, if any
        # but keep the robots...
        #for (key,item) in self.world.iteritems():
        #    self.delete(item.itemid)  # deletes from the canvas
        #self.world = {}
        self.delete('all') # ... but will also delete any robots...
        self.movables = []

        # open the file
        # should do some sanilty checking here...
        mapfile = open(filename, 'r')
    
        prevx = 0
        prevy = 0

        max_x_found = -1000000.0
        max_y_found = -1000000.0
        min_x_found =  1000000.0
        min_y_found =  1000000.0
        
        for line in mapfile:
            line = line[0:line.find('#')]  # strip comment
            # strip whitespace and replace tabs with spaces
            line = line.strip().replace('\t',' ')  
            # get just the space-delimited tokens
            linedata = [x for x in line.split(' ') if x != '']

            # print "linedata is", linedata
            # if empty, continue
            if len(linedata) == 0: continue
        
            # check the type field
            if linedata[0] == 'LINE':
                if linedata[1] == 'PREV':
                    # create linked segment
                    x1 = prevx
                    y1 = prevy
                    x2 = float(linedata[2])
                    y2 = float(linedata[3])
                    # colors
                    r = float(linedata[4])
                    g = float(linedata[5])
                    b = float(linedata[6])

                else:
                    # create new segment
                    x1 = float(linedata[1])
                    y1 = float(linedata[2])
                    x2 = float(linedata[3])
                    y2 = float(linedata[4])
                    # colors
                    r = float(linedata[5])
                    g = float(linedata[6])
                    b = float(linedata[7])

                # add this wall line...
                tmpname = MovableLine(self,
                                      endpoints=[(x1,y1),(x2,y2)], 
                                      colorstr=("#%02x%02x%02x" % (r, g, b)) ) 

                prevx = x2
                prevy = y2
                if x1 < min_x_found:  min_x_found = x1
                if y1 < min_y_found:  min_y_found = y1
                if x1 > max_x_found:  max_x_found = x1
                if y1 > max_y_found:  max_y_found = y1
                if x2 < min_x_found:  min_x_found = x2
                if y2 < min_y_found:  min_y_found = y2
                if x2 > max_x_found:  max_x_found = x2
                if y2 > max_y_found:  max_y_found = y2

        self.snugSquareFitNoRotation( min_x_found, max_x_found, min_y_found, max_y_found )

        mapfile.close()
        
    def snugSquareFitNoRotation(self, x_min, x_max, y_min, y_max):
        """ this will set self.tfm so that the input rectangle
            is aligned with the window
            this will not change the rotation
            (but does not handle rotation yet)
        """
        yMultiplier = 0.85*self.height/math.fabs(y_max-y_min)
        xMultiplier = 0.85*self.width/math.fabs(x_max-x_min)
        #print 'y,x mults are', yMultiplier, xMultiplier
        scaleMultiplier = min(yMultiplier,xMultiplier)
        # mapdelta = max( (y_max-y_min), (x_max-x_min) )
        # scaleMultiplier = 0.85*min(self.height,self.width)/mapdelta
        # self.tfm.multiplyScales(scaleMultiplier, scaleMultiplier)
        #
        # this preserves the signs of the scales...
        self.tfm.setScalesAbsVal(scaleMultiplier, scaleMultiplier)

        # and set the center appropriate to the map...
        wx = (x_max + x_min)/2.0
        wy = (y_max + y_min)/2.0
        self.tfm.setWorldRotationCenter(wx, wy)
        self.redraw()  # have to redraw whenever self.tfm changes...

    def b1_down(self, event):
        if "Shift_L" in self.keysdown and self.keysdown["Shift_L"] == 1:
            # print "b1 down with shift"
            self.click_b3_down(event)
        # c for camera/rotation
        # t for translation
        # should have r for rotation...
        elif ("c" in self.keysdown and self.keysdown["c"] == 1) or \
             ("t" in self.keysdown and self.keysdown["t"] == 1) or \
             ("z" in self.keysdown and self.keysdown["z"] == 1):
            self.startx = event.x
            self.starty = event.y
        # nonuniform scaling
        # c for camera/rotation
        # t for translation
        elif ("y" in self.keysdown and self.keysdown["y"] == 1) or \
             ("x" in self.keysdown and self.keysdown["x"] == 1):
            self.startx, self.starty = event.x, event.y
            self.b1_move(event)
            

    def b1_move(self,event):
        if "Shift_L" in self.keysdown and self.keysdown["Shift_L"] == 1:
            # print "b1 move with shift"
            self.click_b3_move(event)

        elif "z" in self.keysdown and self.keysdown["z"] == 1:
            self.endx = event.x
            self.endy = event.y
            #create a box
            self.delete('temporary_box')
            self.create_polygon(self.startx, self.starty,
                                self.startx, self.endy,
                                self.endx, self.endy,
                                self.endx, self.starty,
                                tag = 'temporary_box', fill = "", outline = 'red')

        elif ("c" in self.keysdown and self.keysdown["c"] == 1) or \
             ("t" in self.keysdown and self.keysdown["t"] == 1):
            self.endx = event.x
            self.endy = event.y
            # create a line in pixel space...
            self.delete('temporary_line')
            self.create_line(self.startx,self.starty,self.endx,self.endy,
                                         tag='temporary_line', fill='purple')
                                         
        elif ("y" in self.keysdown and self.keysdown["y"] == 1) or \
             ("x" in self.keysdown and self.keysdown["x"] == 1):
            self.delete('circle')
            x, y = self.width/2.0, self.height/2.0
            radius = self.length((x,y),(event.x,event.y)) 
            self.create_oval(x - radius, y - radius, x + radius, y + radius, 
                             tag="circle", outline="purple")
            # create a line in pixel space...
            self.delete('temporary_line')
            if ("y" in self.keysdown and self.keysdown["y"] == 1):
                self.create_line(x,y-radius,  # from the center
                                 x,y+radius, # for our y extent
                                 tag='temporary_line', fill='purple',
                                 width=3)
            else:
                self.create_line(x-radius,y,  # from the center
                                 x+radius,y, # for our y extent
                                 tag='temporary_line', fill='purple',
                                 width=3)


    def b1_up(self,event):
        #print "up event at pixel coordinate", event.x, event.y
        #print "up event.keysym is", event.keysym
        
        if "Shift_L" in self.keysdown and self.keysdown["Shift_L"] == 1:
            self.click_b3_up(event)
            
        elif "Control_L" in self.keysdown and self.keysdown["Control_L"] == 1:
            (wx,wy) = self.tfm.transformPixelToWorld((event.x, event.y))
            self.tfm.setWorldRotationCenter(wx, wy)
            self.redraw()

      

        elif "z" in self.keysdown and self.keysdown["z"] == 1:
            self.endx = event.x
            self.endy = event.y
            self.delete('temporary_box')
            self.box_zoom(event)
            
        elif "t" in self.keysdown and self.keysdown["t"] == 1:
            #print 'Translating...'
            self.endx = event.x
            self.endy = event.y
            # delete old line
            self.delete('temporary_line')
            sx, sy = self.tfm.transformPixelToWorld( (self.startx,self.starty) )
            #print "starting coordinates are (wx,wy) = ", (sx, sy)
            ex, ey = self.tfm.transformPixelToWorld( (self.endx,self.endy) )
            #print "ending coordinates are (ex,ey) = ", (ex, ey)
            self.tfm.deltaWorldRotationCenter( (sx-ex), (sy-ey) )
            self.redraw() # need to redraw after tfm changes!
            
        elif ("y" in self.keysdown and self.keysdown["y"] == 1) or \
             ("x" in self.keysdown and self.keysdown["x"] == 1):
            self.delete('circle')
            self.delete('temporary_line')
            x, y = self.width/2.0, self.height/2.0
            radius_stop = self.length((x,y),(event.x,event.y)) 
            radius_start = self.length((x,y),(self.startx, self.starty))
            if radius_start == 0.0: scaleMultiplier = 10.0
            else: scaleMultiplier = radius_stop/radius_start
            if ("y" in self.keysdown and self.keysdown["y"] == 1) :
                self.tfm.multiplyScales(1.0, scaleMultiplier)
            else:
                self.tfm.multiplyScales(scaleMultiplier,1.0)
            self.redraw()
            
        elif "c" in self.keysdown and self.keysdown["c"] == 1:
            self.endx = event.x
            self.endy = event.y
            # delete old line
            self.delete('temporary_line')
            wx, wy = self.tfm.transformPixelToWorld( (self.startx,self.starty) )
            # print "world coordinates are (wx,wy) = ", (wx, wy)
            # compute the theta in world space!
            ex, ey = self.tfm.transformPixelToWorld( (self.endx,self.endy) )
            thr = math.atan2( ey-wy, ex-wx)
            thd = (180.0/math.pi) * thr
            # create a camera!
            # self.addMovable...
            self.redraw()
            
        elif "p" in self.keysdown and self.keysdown["p"] == 1:  
            # if 'p' is pressed, we print the coordinates
            #print "\npixel coordinates are (px,py) = ", event.x, event.y
            wx, wy = self.tfm.transformPixelToWorld( (event.x,event.y) )
            print("click at world coordinates of (wx,wy) = ", wx, wy)

        elif "s" in self.keysdown and self.keysdown["s"] == 1:  
            # if 's' is pressed, we try to toggle the cell clicked
            #print 's' 
            wx, wy = self.tfm.transformPixelToWorld( (event.x,event.y) )
            row = int(wy)
            col = int(wx)
            try:
                w = _getwin()
                #print w
                oldcellvalue = w.canv.referenceToGraphicsData[row][col]
                #print 'oldcell value is', oldcellvalue
                w.canv.referenceToGraphicsData[row][col] = 1-oldcellvalue
                #print 'hi1'
                w.showList( w.canv.referenceToGraphicsData )
            except:
                #print 'error!'
                #print sys.exc_info()[0]
                print()
                print('No square detected at (row, col) = (', row, ',', col, ')')
                print()
            #print "click at world coordinates of (wx,wy) = ", wx, wy
            pass

    def click_b2_down(self, event):
        pass

    def click_b2_move(self, event):
        pass

    def click_b2_up(self, event):
        pass

    def length(self, pt1, pt2):
        return math.sqrt( (pt1.x-pt2.x)**2 + (pt1.y-pt2.y)**2 )

    def click_b3_down(self, event):
        self.startx, self.starty = event.x, event.y
        self.click_b3_move(event)

    def click_b3_move(self, event):
        self.delete('circle')
        x, y = self.width/2.0, self.height/2.0
        radius = self.length((x,y),(event.x,event.y)) 
        self.create_oval(x - radius, y - radius, x + radius, y + radius, tag="circle", outline="purple")

    def click_b3_up(self, event):
        """ scaling... """
        self.delete('circle')
        x, y = self.width/2.0, self.height/2.0
        radius_stop = self.length((x,y),(event.x,event.y)) 
        radius_start = self.length((x,y),(self.startx,self.starty))
        if radius_start == 0.0: scaleMultiplier = 10.0
        else: scaleMultiplier = radius_stop/radius_start
        self.tfm.multiplyScales(scaleMultiplier, scaleMultiplier)
        self.redraw()

    def box_zoom(self, event):
        """ Zooming... """
        self.delete('temporary_box')
        #center view
        #self.startx, self.starty = event.x, event.y
        x = (self.startx + self.endx)/2
        y = (self.starty + self.endy)/2
        (wx,wy) = self.tfm.transformPixelToWorld((x, y))
        self.tfm.setWorldRotationCenter(wx, wy)
        #Zoom
        x = abs(self.startx - self.endx)
        y = abs(self.starty - self.endy)
        screenwidth = self.width
        screenheight = self.height
        xscale = screenwidth/x
        yscale = screenheight/y
        if(xscale < yscale):
            scaleMultiplier = xscale #math.sqrt(xscale*xscale)
        else:
            scaleMultiplier = yscale #math.sqrt(yscale*yscale)
        #scaleMultiplier = math.minimum(xscale, yscale)
        self.tfm.multiplyScales(scaleMultiplier, scaleMultiplier)
        self.redraw()

    def redraw(self):
        """ this goes through the dictionary and recomputes the
            pixel coordinates
        """
        #for (key,item) in self.movables.iteritems():
        for item in self.movables:
            item.updatePixelCoords()

    def addMovable(self, m):
        # check m's name or itemid - if already there, replace
        # self.movables[m.tag] = m
        # self.movables[m.itemid] = m
        # self.redraw()
        self.movables.append(m)
        
class CS5Canvas(ErdosCanvas):
    """ a class to handle displaying various graphical objects
        (at least initially)
    """
    def __init__(self,master=None):
        """ the constructor for the CS5Canvas class """
        ErdosCanvas.__init__(self,master)
        self.setColors()
        self.nowShowing = []
        self.nextrow = 0  # holds the next vertical value at
        # which to put a row of squares...

        
    def setColors(self, colorDictionary={}):
        """ sets up a mapping from arbitrary data to color strings """
        # here is a default
        if colorDictionary == {}:
            self.colorDictionary = {0:"white", 1:"red", "default":"blue"}
        else:
            self.colorDictionary = colorDictionary
            # check that "default" is defined...  
            
    def setColor(self, data, colorstring):
        """ sets up a mapping from arbitrary data to a color string """
        self.colorDictionary[data] = colorstring
            
    def clear(self):
        """ clears the canvas of its items and sets the nextrow to 0 
        """
        self.delete('all')
        self.nextrow = 0
    
            
    def lookup( self, colordatum, newColors = {} ):
        """ handles lots of different types of color data """
        #print "colordatum:", colordatum, "newColors:", newColors
        # if there is a color function, apply it...

        # leave strings alone
        if type(colordatum) is type(''):
            return colordatum
        if type(colordatum) is type(()) and len(colordatum) == 3:
            # treat as r,g,b from 0 to 255 if the first is an int
            # and from 0.0 to 1.0 if the first is a float
            r, g, b = colordatum
            if type(r) is int or type(r) is long:
                r = int(max(0,r))
                r = int(min(255,r))
                g = int(max(0,g))
                g = int(min(255,g))
                b = int(max(0,b))
                b = int(min(255,b))
                return '#%02x%02x%02x' % (r,g,b)
            if type(r) is float:
                r = max(0.0,r)
                r = min(1.0,r)
                g = float(max(0.0,g))
                g = float(min(1.0,g))
                b = float(max(0.0,b))
                b = float(min(1.0,b))
                return '#%02x%02x%02x' % (int(r*255.99),
                                          int(g*255.99),
                                          int(b*255.99))
                                          
        # otherwise, try to look it up in the dictionary
        self.tempDict = newColors
        if colordatum in self.tempDict:
            # new 11/11/07 - change colorDictionary to include tempDict's entries
            self.colorDictionary[colordatum] = self.tempDict[colordatum]
            return self.tempDict[colordatum]
        if colordatum in self.colorDictionary:
            return self.colorDictionary[colordatum]
        else:
            return self.colorDictionary["default"]
            
    # def show1d - deletes/rescales, add1d - adds/recenters? draw1d - 
    # def show2d - deletes/rescales
    
    def add1d( self, L ):
        """ if self.nextrow == 0, we add a row and rescale
            if not, we add a row and recenter
            if the length changes, we start again...
        """
        # might want to handle tuples and strings by casting them to lists?
        if type(L) is not type([]) or len(L) == 0:
            print('the input to CS5Canvas.show must be a nonempty list')
            print('in this case, L =', L, ', was input.  Returning...')
            
        # we will treat L as a one-dimensional list now
        N = len(L)
        oldN = len(self.nowShowing)
        if N != oldN or self.nextrow == 0:
            self.nextrow = 0
            # we need to delete the old and create the new...
            self.delete('all')  # remember, self is a Tkinter.Canvas
            self.nowShowing = self.create1d( L, self.nextrow )
            self.snugSquareFitNoRotation( 0, N, 0, 1 ) # should place at top
            
        else: # add to self.nextrow
            self.nowShowing = self.create1d( L, self.nextrow )
            #self.snugSquareFitNoRotation( 0, N, 0, 1 ) # should place at top
        
        wx = N/2.0
        wy = 0.5 + self.nextrow
        #print 'new wx, wy!'
        #print 'old scalex, scaley', self.tfm.scalex, self.tfm.scaley
        self.tfm.setWorldRotationCenter(wx, wy)
        #print 'old scalex, scaley', self.tfm.scalex, self.tfm.scaley
        self.redraw()  # have to redraw whenever self.tfm changes...
        self.nextrow += 1


    def show2d( self, L, newColors):
        """ display the list L as a set of rectangles
              input L: a list of data
            if L's data are strings, it passes those
            strings on and hopes they are colors...
            otherwise it looks up the data in the
            self.colorDictionary data member, using 
            self.colorDictionary["default"] if it's not there.
            vertical is the lower y-coordinate of the row of squares
            
            returns the list of canvas items it creates (or has changed...)
        """
        # might want to handle tuples and strings by casting them to lists?
        if type(L) is not type([]) or len(L) == 0:
            print('the input to CS5Canvas.show2d must be a nonempty list')
            print('in this case, L =', L, ', was input. Going to default.')
            L = [ [0,1], [1,0] ]  # a 2x2 default list

        firstRow = L[0]
        if type(firstRow) is not type([]) or len(firstRow) == 0:
            print('the input to CS5Canvas.show2d must be a nonempty list')
            print('in this case, L =', L, ', was input. Using default data.')
            L = [ [2,1], [1,2] ]

        # we keep a copy of the reference to the current data,
        # so that a mouse click will change the actual data...
        self.referenceToGraphicsData = L

        needToRecreateGraphics = False

        #print 'self.nowShowing is', self.nowShowing
        #print 'self.nowShowing[0] is', self.nowShowing[0]
        NROWS = len(L)
        NCOLS = len(L[0])

        # is self.nowShowing of the corect format?
        if len(self.nowShowing) < 1:
            needToRecreateGraphics = True
            
        elif type(self.nowShowing[0]) is not type([]):
            needToRecreateGraphics = True

        else:
            # we will treat L as a one-dimensional list now
            oldNROWS = len(self.nowShowing)
            oldNCOLS = len(self.nowShowing[0])
            if NROWS != oldNROWS or NCOLS != oldNCOLS:
                needToRecreateGraphics = True

        if needToRecreateGraphics:
            # we need to delete the old and create the new...
            self.delete('all')  # remember, self is a Tkinter.Canvas
            self.nowShowing = self.create2d( L, 0, NROWS, NCOLS, newColors )
            self.snugSquareFitNoRotation( 0, NCOLS, 0, NROWS )
            self.nextrow = 0
            
        else: # the length of L has not changed!
            # just change the colors
            # we could, in fact, change only the colors that need changing
            for row in range(NROWS):
                for col in range(NCOLS):
                    self.nowShowing[row][col].setColorstr( \
                        self.lookup(L[row][col],
                        newColors) )
                
            
    def show1d( self, L, newColors):
        """ display the list L as a set of rectangles
              input L: a list of data
            if L's data are strings, it passes those
            strings on and hopes they are colors...
            otherwise it looks up the data in the
            self.colorDictionary data member, using 
            self.colorDictionary["default"] if it's not there.
            vertical is the lower y-coordinate of the row of squares
            
            returns the list of canvas items it creates (or has changed...)
        """
        # might want to handle tuples and strings by casting them to lists?
        if type(L) is not type([]) or len(L) == 0:
            print('the input to CS5Canvas.show must be a nonempty list')
            print('in this case, L =', L, ', was input.  Returning...')

        # make self.nowShowing one-dimensional, if it's not
        if len(self.nowShowing) > 0:
            if type(self.nowShowing[0]) is type([]):
                self.nowShowing = []  
            
        # set up vertical
            
        # we will treat L as a one-dimensional list now
        N = len(L)
        oldN = len(self.nowShowing)
        if N != oldN:
            # we need to delete the old and create the new...
            self.delete('all')  # remember, self is a Tkinter.Canvas
            self.nowShowing = self.create1d( L, 0 , newColors)
            self.snugSquareFitNoRotation( 0, N, 0, 1 )
            self.nextrow = 0
            
        else: # the length of L has not changed!
            # just change the colors
            # we could, in fact, change only the colors that need changing
            for i in range(N):
                self.nowShowing[i].setColorstr( self.lookup(L[i], newColors) )
                
    def create1d( self, L, y, newColors):
        """ creates squares from y to y+1 according to L
            returns the newly created canvas items in a list
        """
        return [ MovableRect(self,
                             tlbr_endpoints=[(x,y),(x+1,y+1)],
                             colorstr=self.lookup(L[x], newColors) )
                 for x in range(len(L)) ]

    def create2d( self, L, y, NROWS, NCOLS, newColors):
        """ creates squares from y to y+1 according to L
            returns the newly created canvas items in a list
        """
        twoDarray = []
        for row in range(NROWS):
            twoDarray.append([ MovableRect(self,
                                 tlbr_endpoints=[(x,y+row),(x+1,y+row+1)],
                                 colorstr=self.lookup(L[row][x], newColors) ) \
                                 for x in range(NCOLS) ])
        return twoDarray
        
        
class CS5Frame(Frame):
    """ There was a split here to handle scroll bars, but
        then I decided against scroll bars.
        Yet the two classes (CS5Frame and CS5Win) remain...
    """
    
    def __init__(self,master=None):
        """ CS5Frame constructor """
        Frame.__init__(self,master)
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+E+W)
        self.canv = CS5Canvas( self )
        self.canv.grid( row=0, column=0, sticky=N+S+E+W )
        self.canv.tfm.setScales(1,-1)
        self.canv.tfm.setWorldRotationCenter(0,0)

    def updateList(self, L = None):
        """ this is for evolving in time... probably not for CS 5 this year... """
        if not L:
            # show1d
            self.canv.add1d( [ [random.randrange(0,256) for i in range(3)] for i in range(5) ] ) 
        else:
            self.canv.add1d( L )
        #self.quit()
        
    def showList(self, L = None, newColors = {}):
        """ displays a list L as a row of squares of color """
        if not L:
            # we'll just make up a 3x3 with 3 random colors...
            self.canv.show2d( [ [random.randrange(0,3) for i in range(3)] for i in range(3) ] ) 
        # is it one- or two- dimensional?
        elif type(L) is type([]):
            if len(L) > 0:
                if type(L[0]) is type([]):  # 2d
                    self.canv.show2d( L , newColors)
                else:
                    self.canv.show1d( L , newColors)
            else:
                print('The list is empty! Not displaying...')
        #self.quit()
        
    def makeAPlot(self,Y,leftx,dx,plottype='s', color = 'black'):
        """ this plotting function has four options (final input):
            's'  for line segments
            'p'  for points
            'recL' for rectangles with left endpoints on the curve
            'recU' for rectangles with right endpoints on the curve
        color allows the user to change the color of the plotted line
        """
        # hmmm...
        N = len(Y)
        if N < 2:
            print('Cannot plot fewer than 2 points')
            return
        if dx == 0.0:
            print('Cannot plot with a stepsize of 0.0')
            return
        
        # make sure the type is a string
        if type(plottype) != type(''):
            print('Unrecognized plottype:', plottype)
            plottype = 's'
        
        if 'recL' in plottype:
            plotElements = [ MovableRect(self.canv, 
                                         tlbr_endpoints=[(leftx+dx*i,Y[i]),
                                                         (leftx+dx*(i+1),0)], 
                                         colorstr='blue') for i in range(N) ]
        if 'recU' in plottype:
             plotElements = [ MovableRect(self.canv, 
                                         tlbr_endpoints=[(leftx+dx*i,Y[i+1]),
                                                         (leftx+dx*(i+1),0)], 
                                         colorstr='cyan') for i in range(N-1) ]
            
        if 's' in plottype:
            # only go up to N-1 since we are adding one already to
            # obtain the right endpoint of each segment
            plotElements = [ MovableLine(self.canv, [ [leftx+dx*i,Y[i]],
                             [leftx+dx*(i+1),Y[i+1]] ], colorstr = color)  for i in range(N-1) ]
                             
        if 'p' in plottype:
            plotElements = [ MovablePoint(self.canv, cx=leftx+dx*i, cy=Y[i],
                              colorstr='red') for i in range(N) ]
           
                         
        # values for scaling
        maxy = max(Y)
        miny = min(Y)
        # include the x-axis if rectangles were drawn
        if 'rec' in plottype:
            maxy = max(maxy,0.0)
            miny = min(miny,0.0)
        # the x limits are easier
        minx = leftx
        maxx = leftx + N*dx
        #add x and y axes
        plotElements.extend([MovableLine(self.canv, [[-1000 + minx,0],[1000 + maxx, 0]], colorstr = 'grey'), MovableLine(self.canv, [[0,-1000 + miny],[0, 1000 + maxy]],colorstr = 'grey')])
        self.canv.tfm.setScales(1,-1)
        self.canv.snugSquareFitNoRotation( minx, maxx, miny, maxy )
        #self.canv.redraw()
        return
        
        


### 
#
#   All of this stuff is adapted from turtle.py and graphics.py
#
#   These are 
#
###

import time   # to wait for a mouse click...

# If we reload, this will close any window that was remaining from before...
try:
    global _window
    w = _window
    if w != None:
        # if the window exists here, we destroy it to complete the reload
        # of this module (it must be a reload...)
        w.tkroot.destroy()  
except NameError:
    #print 'No window... setting to None'
    pass

#
# Here is the global window object, _window
#
_window = None

def _getwin():
    """ a utility function to obtain the global window 
        and create it if it doesn't yet exist
    """
    global _window
    w = _window
    if w == None: w = CS5Win()
    _window = w
    return w
    
#
# I had trouble when this class was above the global _window declaration...
#
class CS5Win(CS5Frame):  
    """ CS5Win is meant to be an automatically appearing window, as needed """
    # as mentioned above in CS5Frame, it probably should not be separate...
    # these two classes (CS5Win and CS5Frame) should be combined
    
    def __init__(self):
        """ CS5Win's constructor """
        global _window
        #if _window is None: # for next two lines?
        self.tkroot = Tk()
        self.tkroot.protocol("WM_DELETE_WINDOW", self._destroy)
        self.tkroot.title('CS 5 Window')
        CS5Frame.__init__(self, self.tkroot)
        _window = self
        # make sure we're watching for clicks (on top of other 
        # callbacks that might also be watching...
        self.bind_all("<Button>", self.onClick, add='+')
        
    def onClick(self, event):
        wx, wy = self.canv.tfm.transformPixelToWorld( (event.x,event.y) )
        self.clickedWorldX = wx
        self.clickedWorldY = wy
        
    def clearLastMouseClick(self):
        self.clickedWorldX = None
        self.clickedWorldY = None

    def _destroy(self):
        """ _destroy sets _window to None """ 
        #if self.idlerID:
        #    self.after_cancel(self.idlerID)
        global _window
        _window = None
        self.tkroot.destroy()
    
#
# These next three functions are for Lab 2
#
    
def plot(Y,low=0.0,hi=1.0,s='s', color = 'black'):
    """ plot draws line segments between the values in the list Y
        The x coordinates are evenly spaced in [low,hi)
        The coordinate system is chosen to leave a margin around the plot
    """
    w = _getwin()
    LY = len(Y)
    if LY == 0: return
    dx = (hi-low)/float(LY)
    w.makeAPlot(Y,low,dx,s, color)
    w.update()
    #w.mainloop()
    
def done():
    w = _getwin()
    w.mainloop()

def update():
    w = _getwin()
    w.update()       # forces an update of the graphics...
    

def clear():
    """ erases everything and resets the coordinate system """
    w = _getwin()
    w.canv.tfm.setScales(1,-1)
    w.canv.tfm.setWorldRotationCenter(0,0)
    w.canv.tfm.setPixelRotationCenter(w.canv.width/2, w.canv.height/2)
    w.canv.clear()
    
def setColor(x,colorstring):
    """ sets the color of item x """
    w = _getwin()
    w.canv.setColor(x,colorstring)
    
#
# These next three functions are for Labs
#

def openWindow():
    w = _getwin()
    return
    
def show(L, newColors = {}): 
    """ displays a 1d line of colored squares """
    w = _getwin()
    w.showList(L, newColors)
    w.update()       # forces an update of the graphics...
    #w.mainloop()

def showAndClickInIdle(L, newColors = {}): 
    """ displays a 1d line of colored squares """
    w = _getwin()
    w.showList(L, newColors)
    w.update()       # forces an update of the graphics...
    w.mainloop()

    
def getKeysDown():
    """ returns the string of keys currently pressed """
    w = _getwin()
    d = w.canv.keysdown # get dictionary
    L = []  # list of active keys
    for i in d.keys():
        if d[i]: L.append( i )  # make sure they're down
    return ''.join(L)   # return a string
    

def winput(promptstr=''): 
    """ winput gets a mouse click and returns the world coordinates """
    w = _getwin()
    if not w:
        print('No window available!')
        return [ 0, 0 ]
    if promptstr: print(promptstr,)
    w.clearLastMouseClick()
    while True:
        cx = w.clickedWorldX
        cy = w.clickedWorldY
        if cx != None and cy != None: break
        w.update()
        time.sleep(0.1)
    if promptstr: print
    return [ cx, cy ]
    
def sqinput(promptstr=''):
    """ sqinput gets a click and returns the index of the square clicked on """
    w = _getwin()
    if not w:
        print('No window available!')
        return -1
    N = len(w.canv.nowShowing)
    cx, cy = winput(promptstr)
    if N == 0: return -1
    sqnum = int(cx)
    if sqnum <= 0: return 0
    if sqnum >= N: return N-1
    return sqnum


def sqinput2(promptstr=''):
    """ sqinput gets a click and returns the index of the square clicked on """
    w = _getwin()
    if not w:
        print('No window available!')
        return -1
    NROWS = len(w.canv.nowShowing)
    try:
        NCOLS = len(w.canv.nowShowing[0])
    except:
        print('The data does not seem 2d.')
        print('Try using sqinput instead.')
        return -1,-1
    cx, cy = winput(promptstr)
    if NROWS == 0 or NCOLS == 0: return -1, -1
    
    colnum = int(cx)
    if colnum <= 0: colnum = 0
    if colnum >= NCOLS: colnum = NCOLS-1

    rownum = int(cy)
    if rownum <= 0: rownum = 0
    if rownum >= NROWS: rownum = NROWS-1
    
    return colnum, rownum
    
# I don't know why Y seems to be changing, but we'll set it to None...
Y = None

# I just like to have this for pasting into the console...
# import csplot ; reload(csplot) ; from csplot import *



