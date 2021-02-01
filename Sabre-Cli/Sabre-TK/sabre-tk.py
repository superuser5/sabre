#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk 
from multiprocess import Process #needs pip installed
import os
import subprocess
#from PIL import Image, ImageTK # needs pip installed

tocIP = ''
tocUser = ''
tocConnections = ''

#def sabreClient(u,s):
def sabreClient():
    #user = u
    #server = s
    os.system('/usr/bin/qterminal')


#def startClient(u,s):
def startClient():
    #user = u
    #server = s 
    #start terminal with sabre-cli in seperate window with multiprocess
    p = Process(target=sabreClient) #, args=('user','server'))
    p.start()
    #p.join()
    toc_connections["state"] = "normal"
    toc_connections.delete("1.0", "end")
    connectionstr = subprocess.check_output("netstat | grep 22", shell=True)
    toc_connections.insert("1.0", connectionstr)
    toc_connections["state"] = "disabled"

root = tk.Tk() 
root.title("Sabre Client")

style = ttk.Style(root)
#print(style.theme_names())
#style.theme_use("default")

tocConnFrame = ttk.Frame(root)
tocConnFrame.pack(side="bottom", fill="both", expand=True)
toc_connections = tk.Text(tocConnFrame)
toc_connections.insert("1.0", "Connections to TOC's listed below........")
toc_connections["state"] = "disabled"
#toc_connections.pack(side='top', fill="both", ipadx=(5), ipady=(5), expand=True)
toc_connections.grid(row=0, column=0, sticky="nsew")
toc_connections_scroll_V = ttk.Scrollbar(tocConnFrame, orient="vertical", command=toc_connections.yview) #Virtical Scroll for connection output
toc_connections_scroll_V.grid(row=0, column=1, sticky="ns")
toc_connections_scroll_H = ttk.Scrollbar(tocConnFrame, orient="horizontal", command=toc_connections.xview) #Horizontal Scroll for connection output
toc_connections_scroll_H.grid(row=1, column=0, sticky="ew")

toc = ttk.Frame()
toc.pack(side="left", fill="both", expand=True)

tocIPFrame = ttk.Frame(toc)
tocIPFrame.pack(side="top", fill="both", expand=True)
toc_IP = ttk.Label(tocIPFrame, text="SABRE TOC IP: ")
toc_IP.pack(side="left", padx=(0,10))
toc_IP_Entry = ttk.Entry(tocIPFrame, width=15, textvariable=tocIP)
toc_IP_Entry.pack(side="right", fill="x", expand=True)

tocUserFrame = ttk.Frame(toc)
tocUserFrame.pack(side="bottom", fill="both", expand=True)
toc_User = ttk.Label(tocUserFrame, text="SABRE TOC USER: ")
toc_User.pack(side="left", padx=(0,10))
toc_User_Entry = ttk.Entry(tocUserFrame, width=15, textvariable=tocUser)
toc_User_Entry.pack(side="right", fill="x", expand=True)


toc_IP_Entry.focus()

connect_button = ttk.Button(root, text="Connect", command=startClient)
connect_button.pack(side="left", fill="both", expand=True)
#getting contents of the IP and USER
#ip = toc_IP_Entry.get('1.0', 'End')
#user = toc_User_Entry.get('1.0', 'End')

quit_button = ttk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(side="right", fill="both", expand=True)

root.mainloop()
