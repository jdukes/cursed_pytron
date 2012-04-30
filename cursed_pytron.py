#!/usr/bin/env python

#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------

import curses, random, os
from time import sleep
from ConfigParser import ConfigParser
from curses.wrapper import wrapper as curse

#-------------------------------------------------------------------------------
# defs (colors and directions)
#-------------------------------------------------------------------------------

BLACK = 1
RED = 2
GREEN = 3
YELLOW = 4
BLUE = 5
MAGENTA = 6
CYAN = 7
WHITE = 8

UP = curses.KEY_UP
DOWN = curses.KEY_DOWN
LEFT = curses.KEY_LEFT
RIGHT = curses.KEY_RIGHT

#-------------------------------------------------------------------------------
# initialize config
#-------------------------------------------------------------------------------

config = ConfigParser()
config.read("config")

#-------------------------------------------------------------------------------
# primary functions 
#-------------------------------------------------------------------------------

def wall_crash_check(i,max):
    if i <= 0:
        return True
    elif i >= max:
        return True
    else:
        return None

#-------------------------------------------------------------------------------

class light_cycle:
    def __init__(self,y,x,cfg_section):
        self.__description__="<light cycle object>"
        self.key={}
        self.trail=[]
        self.has_crashed=False
        self.y=y
        self.x=x
        self.direction=config.get(cfg_section,"direction")
        try:
            self.color=eval(config.get(cfg_section,"color").upper())
        except:
            print "color error moron, fix your config file!"
            os._exit(1)
        self.name=config.get(cfg_section,"name")
        for i in ["up","down","left","right"]:
            key=config.get(cfg_section,"key_"+i)
            try:
                key_val=eval(key.upper())
            except:
                try:
                    key_val=ord(key)
                except:
                    print "key error moron, fix your config file!"
                    os._exit(1)            
            self.key[i]=key_val

    def control(self,c):
        if c > 0:
            if c == self.key["up"] and not self.direction == "down" :
                self.direction="up"
            if c == self.key["down"] and not self.direction == "up" :
                self.direction="down"
            if c == self.key["left"] and not self.direction == "right" :
                self.direction="left"
            if c == self.key["right"] and not self.direction == "left" :
                self.direction="right"

    def move(self):
        if self.direction == "up":
            self.y-=1
        elif self.direction == "down":
            self.y+=1
        elif self.direction == "right":
            self.x+=1
        elif self.direction == "left":
            self.x-=1

    def crash_check(self,Y,X,trials=[]):
        if wall_crash_check(self.x,X) or wall_crash_check(self.y,Y):
            self.has_crashed=True
        for trail in trials:
            if trail.count((self.y,self.x)):
                self.has_crashed=True                
        if not self.has_crashed:
            self.trail.append((self.y,self.x))
        return self.has_crashed

    def explode(self,win,Y,X):
        if self.y==0:
            self.y=1
        if self.x==0:
            self.x=1
        if self.x==0:
            self.x=1
        if self.y==Y:
            self.y=Y-2
        if self.x==X:
            self.x=X-2
        for i in range(-1,2): 
            for j in range(-1,2): 
                win.move(self.y+j,self.x+i)
                win.addch(' ',random.randint(1,10))
    def draw(self,win):
        win.addch(self.y,self.x,'0',curses.color_pair(self.color))
    def clear_trail(self,win):
        for i in self.trail:
            win.delch(i)
    def __del__(self):
        del(self.y)
        del(self.x)
        del(self.direction)
        del(self.color)
        del(self.name)
        del(self.trail)
    def __repr__(self):
        return "<light cycle object>"
    def __str__(self):
        return "<light cycle object>"
    
#-------------------------------------------------------------------------------

def main(stdscr):
    for i in range(8):
        curses.init_pair(i+1,i,curses.COLOR_BLACK)
    curses.curs_set(0)
    win=curses.newwin(0,0)
    Y,X = win.getmaxyx()
    Y,X = Y-1,X-1
    win.addstr(Y/2-5,X/2-9,"EXTREME Pointless Tron!!!" ,curses.color_pair(RED))
    win.addstr(Y/2,X/2-4,"y: %d x: %d" % (Y,X) ,curses.color_pair(RED))
    win.refresh()
    sleep(1)
    c=ord('Y')

    while c==ord('y') or c==ord('Y'):
        stdscr.timeout(0)
        player1=light_cycle(Y/2,(X/2)-10,"player1")
        player2=light_cycle(Y/2,(X/2)+10,"player2")
        stdscr.erase()
        win.erase()
        r=range(4)
        r.reverse()
        for i in r:
            win.addch(Y-5,X/2-1,"%d" % i,
                      curses.color_pair(curses.COLOR_RED+1))
            win.refresh()
            sleep(0.01)
        win.delch(Y-5,X/2-1)
        win.refresh()
        has_winner=False
        while not has_winner:
            win.box()
            c=stdscr.getch()
            for i in [player1,player2]:
                i.control(c)
                i.move()
                if i.crash_check(Y,X,[player1.trail, player2.trail]):
                    i.explode(win,Y,X)
                    win.addstr(Y/2-5,X/2-9,"YOU SUCK %s!!!" % i.name,
                               curses.color_pair(curses.COLOR_RED+1))
                    has_winner=True
                else:
                    i.draw(win)
            win.refresh()
            stdscr.noutrefresh()
            sleep(.1)
            win.refresh()

        stdscr.timeout(-1)
        win.addstr(Y/2,X/2-4,"Play again??(y/n)",curses.color_pair(RED))
        win.refresh()
        while not c==ord('y') and not c==ord('Y') and not c==ord('N') and not c==ord('n'):
            c=stdscr.getch()

if __name__ == "__main__":
    curse(main)

