import io
import os
import PySimpleGUI as sg
from PIL import Image
import cv2
import numpy as np
import webbrowser

def detect(sqr):
    pieces = ['wb','wk','wq','wn','wr','wp','b','k','q','n','r','p','e','wb1','wk1','wq1','wn1','wr1','wp1','b1','k1','q1','n1','r1','p1','e1','wcb','wck','wcq','wcn','wcr','wcp','cb','ck','cq','cn','cr','cp','wcb1','wck1','wcq1','wcn1','wcr1','wcp1','cb1','ck1','cq1','cn1','cr1','cp1']
    names = ['B' , 'K', 'Q' , 'N' , 'R' , 'P' ,'b' , 'k','q','n','r','p' ,'e','B' , 'K', 'Q' , 'N' , 'R' , 'P' ,'b' , 'k','q','n','r','p','e','B','K','Q','N','R','P','b','k','q','n','r','p','B' , 'K', 'Q' , 'N' , 'R' , 'P' ,'b' , 'k','q','n','r','p']
    values = []
    for piece in pieces:
        template = cv2.imread('chess/'+piece +'.jpg', 0)
        result = cv2.matchTemplate(sqr , template , cv2.TM_SQDIFF_NORMED)
        minV , maxV , minL , maxL = cv2.minMaxLoc(result)
        values.append(minV)
    minv = min(values)
    index = values.index(minv)
    return names[index]

def getLink(imgPath , side):
    inputIMG = cv2.imread(imgPath , 0)
    img2 = cv2.resize(inputIMG , (800,800))       
    h = 0
    w = 0
    sqrs = ""
    for i in range(0,8):
        w = 0
        sqrs = sqrs+"/"
        for j in range(0, 8):
            img3 = img2[h:h+100 , w:w+100]
            sqrs = sqrs + detect(img3)
            w = w+100
        h = h +100
        turn = "w"

    fen = ""
    nbOfE = 0
    for char in sqrs:
        if(char == 'e'):
            nbOfE = nbOfE +1
        else:
            if(nbOfE > 0):
                fen = fen + str(nbOfE)
                nbOfE = 0
            fen = fen + char

    if(nbOfE > 0):
        fen = fen + str(nbOfE)
    if side % 2 == 0:
        turn = "w"
    else:
        turn = "b"
    link = "https://lichess.org/analysis"+fen+"_"+turn+"_KQkq_-_0_1"
    return link

file_types = [("JPEG (.jpg)", ".jpg"),("PNG (.png)" ,".png"),
              ("All files (.)", ".")]
sg.theme('dark blue 3')
def main():
    down = True
    OUTPUT = ""
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File:"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
        [sg.Text("Link:")],[sg.Text(size=(50,2) , key='LINKK')],[sg.Text("",key=("-OUT-"))],[sg.Text("turn?")],
        [sg.Button("White", size=(4,1), button_color=("white", "green"), key="B")],
        [sg.Button("Get Link" , size=(6,1) , button_color=("white" , "green"), key="L")]
    ]
    window = sg.Window("Image Viewer", layout)
    turn = 0
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "L":
            linkText = getLink(filename , turn)
            window.Element('LINKK').Update(linkText)
            webbrowser.open(linkText)
        if event == 'B':
            turn = turn + 1
            down = not down
            window.Element('B').Update(('Black','White')[down], button_color=(('white', ('red', 'green')[down])))
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-OUT-"].update(OUTPUT)
                window["-IMAGE-"].update(data=bio.getvalue())
    window.close()
if __name__ == "__main__":
    main()