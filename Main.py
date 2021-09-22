from pyautogui import *
from keyboard import *
from time import *
from os import *
from threading import *
from tkinter import *
from tkinter.ttk import *

# V 0.37 - [Alpha]
# made by Function(Terry)

#----Variable----#
i=0
cnt=0
log="\n\n[LOG]\n\n"
#name_char=((2109, 1208),(540, 1206),(914, 1204),(770, 1196),(1463, 1202))
name_char=("moira","orisa","reaper","genzi","echo","sigma","mercy","bri","ashe")
kor_char=("모이라","오리사","리퍼","겐지","에코","시그마","메르시","브리기테","에쉬")
select=0
enable=True

#----Variable Function----#

#Function
#V0.1일때 테스트용
def load():
    global i
    global enable
    global log
    #system("cls")
    #print("횟수 : {0}번\t여부 : {1}".format(i,enable))

#클릭 함수
def Auto(pos, enable):
    global select
    if pos!=None:
        findLabel.config(text="Find :True")
        if enable==True:
            before_pos=position()
            load()
            logAdd("select","{0} 클릭".format(kor_char[select]))
            doubleClick(pos)
            sleep(0.5)
            moveTo(before_pos)
    else:
        findLabel.config(text="Find :False")

#로그 추가
def logAdd(event,tell):
    global log
    global enable
    global i

    title=""
    if event=="press":
        title="Key Pressed"
    elif event=="select":
        title="Selected Hero"
    elif event=="bool":
        title="Enable"
    elif event=="cmd":
        title="Command"
    elif event=="err":
        title="Error"
    elif event=="bg":
        title="bgColor"
    else:
        title="Log"

    i+=1
    enableLabel.config(text=("Enable : {0}".format(enable)))
    cntLabel.config(text=("log : {0}".format(i-3)))
    heroLabel.config(text="Hero : {0}".format(kor_char[select]))
    tree.insert('', 'end', text=(i-3), values=(title,tell))

#V0.2일때 테스트용
def change():
    global select
    if select<len(name_char)-1:
        select+=1
    else:
        select=0
    heroLabel.config(text="Hero : {0}".format(name_char[select]))

#키 입력
def wait_press(time, key_name):
    sleep(time)
    press(key_name)
    sleep(0.1)

#명령어 처리/실행
def Command(event):
    global enable
    global cnt
    global name_char
    global select
    known=True
    get=str(commandEntry.get())
    cutLine=get.find(" ")
    if get.find(" ")==-1:
        cmd=get
        arg=None
    else:
        cmd=get[:cutLine]
        arg=get[cutLine+1:]
    if cmd=="enable":
        if arg=="True":
            cnt=0
            enable=True
            logAdd("cmd",arg)
        elif arg=="False":
            cnt=1
            enable=False
            logAdd("cmd",arg)
    elif cmd=="select" or cmd=="hero":
        try:
            if int(arg)<len(name_char) and 0<=int(arg):
                select=int(arg)
                logAdd("cmd",("{0} 선택".format(kor_char[select])))
                sleep(0.15)
        except ValueError:
            for i in range(len(name_char)):
                if arg==name_char[i] or arg==kor_char[i]:
                    select=i
                    logAdd("cmd",("{0} 선택".format(kor_char[select])))
    elif cmd=="log":
        try:
            if arg.find("{")>=0:
                title=arg[arg.find("{")+1:arg.find("}")]
                arg2=arg[arg.find("}")+2:]
                text=arg2[arg2.find("{")+1:arg2.find("}")]
                logAdd(title, text)
        except Exception:
            logAdd("err","log {-title} {-text}")
    elif cmd=="bgcolor":
        try:
            if arg!=None:
                root.configure(bg=arg)
                logAdd("bg",arg)
        except Exception:
            pass
    else:
        known=False

#----Thread----#
#미선택
def auto1():
    while True:
        text="H{0}1.png".format(name_char[select])
        Auto(locateCenterOnScreen(text),enable)

#선택
def auto2():
    while True:
        text="H{0}2.png".format(name_char[select])
        Auto(locateCenterOnScreen(text),enable)

#활성화 / 비활성화
def f7Key():
    global enable
    global cnt
    global i
    while True:
        if is_pressed("f7"):
            logAdd("press","F7")
            if cnt==0:
                enable=False
                logAdd("bool","False")
                cnt=1
            elif cnt==1:
                enable=True
                logAdd("bool","True")
                cnt=0
            sleep(0.5)
            load()

#----GUI/Main----#
load()
th=(Thread(target=f7Key),Thread(target=auto1),Thread(target=auto2))
i=0
for i in range(len(th)):
    th[i].start()

#GUI창 생성
root=Tk()
root.geometry("400x270")
root.resizable(False,False)
root.title("Log")

#로그 갯수
cntLabel=Label(text="log : 0")
cntLabel.place(x=310,y=5)

#활성화 여부
enableLabel=Label(text="Enable : True")
enableLabel.place(x=310,y=25)

#선택된 캐릭터
heroLabel=Label(text="Hero : 모이라")
heroLabel.place(x=310,y=45)

#사진 찾음 여부
findLabel=Label(text="Find : False")
findLabel.place(x=310,y=65)

#커맨드
Label(text="CMD").place(x=0,y=240)

#커맨드 입력
commandEntry=Entry(width=38)
commandEntry.place(x=35,y=240)
commandEntry.bind("<Return>", Command)

#로그
tree=Treeview(columns=["title","text"])
tree.place(x=5,y=5)

tree.column('#0',width=50)
tree.heading("#0", text="Num")

tree.column("title", width=100)
tree.heading("title", text="Title")

tree.column("text", width=150)
tree.heading("text", text="Text")

root.mainloop()
