import tkinter
import os
import ast
import random
from dotenv import load_dotenv
from openai import OpenAI


root=tkinter.Tk()
cvs = tkinter.Canvas(root,width = 2000,height = 1200, bg="white")
cvs2 = None
widgets_but=[]
widgets_tex=[]
ent=[]
cvs.pack()


MODEL = "gpt-6.1-terra"

def create_client():
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        cvs.create_text(
            100, 1300,
            text="OPENAI_API_KEY が設定されていません。.env か環境変数に設定してください。"
        )
        return None

    return OpenAI(api_key=api_key)


client = create_client()


def ask_openai(client, prompt):
    response = client.responses.create(
        model=MODEL,
        input=prompt
    )
    return response.output_text


def disp_aru(u):
    for i in range(len(u)):
        cvs.create_text(500,250+i*150,text=u[i],fill="black",font=("Meiryo",24))

def disp_nai(u):
    for i in range(len(u)):
        cvs.create_text(900,250+i*150,text=u[i],fill="black",font=("Meiryo",24))

def disp_text(a, b):
    tex = tkinter.Entry(font=("Meiryo", 36))
    tex.place(x=a, y=b, width=300, height=100)

    widgets_tex.append(tex)


def get_aru():
    results = []
    for tex in widgets_tex[:3]:
        results.append(tex.get())
    return results


def get_nasi():
    results = []
    for tex in widgets_tex[3:]:
        results.append(tex.get())
    return results

def get_ans():
    ent.append(get_aru())
    ent.append(get_nasi())
    
    prom = f"あなたはあるなしクイズのプロです。以下に共通点があるもの、ないものにそれぞれ分けたリストを表示するので、その共通点が何かを30字以内で答えてください。それでは、問題を表示します。{ent[0]},{ent[1]}"
    ans = ask_openai(client,prom)
    ent.clear()
    disp_ans(ans)

def dispA_again():
    clear_screen()
    displayA()

def disp_ans(ans):
    global cvs2
    cvs2 = tkinter.Canvas(root,width=900,height=200, bg="light gray")
    cvs2.place(x=250,y=700)
    cvs2.create_text(450,50,text=f"回答:{ans}",font=("Meiryo",24))
    but1 = tkinter.Button(text="次の問題へ",font=("Meiryo",24),command=dispA_again)
    but1.place(x=300,y=800,width=200,height=50)
    but2= tkinter.Button(text="やめる",font=("Meiryo",24),command=ret_to_0)
    but2.place(x=850,y=800,width=200,height=50)
    widgets_but.extend([but1,but2])


def get_prob(a=True):
    if a:
        prom="""あなたはあるなしクイズのプロです。
                共通点があるものを３つ、ないものを３つ挙げて、
                その後に「ある」に該当する単語を１つ挙げるタイプのあるなしクイズを解説付きで作ってください。
                ただし、出力形式は次の解答例に従ってください。
                【解答例】[["ある1","ある2","ある3"],["ない1","ない2","ない3"],["判定する単語","解説"]]"""
        prob = ask_openai(client,prom)
        print("probの型:", type(prob))
        print("probの内容:", repr(prob))
        return ast.literal_eval(prob)
    else:
        prom="""あなたはあるなしクイズのプロです。
                共通点があるものを３つ、ないものを３つ挙げて、
                その後に「ない」に該当する単語を１つ挙げるタイプのあるなしクイズを解説付きで作ってください。
                ただし、出力形式は次の解答例に従ってください。
                【解答例】[["ある1","ある2","ある3"],["ない1","ない2","ない3"],["判定する単語","解説"]]"""
        prob=ask_openai(client,prom)
        print("probの型:", type(prob))
        print("probの内容:", repr(prob))
        return ast.literal_eval(prob)

def judge(u):
    if u:
        return disp_cor("正解!")
    else:
        return disp_cor("不正解...")

def disp_but(b,exp, a=True):
    cvs.create_text(700,800,text=f"{b}はどっち?",fill="black",font=("Meiryo",30))

    if a:
     but1=tkinter.Button(text="ある",font=("Meiryo",24), command=lambda: disp_cor(x=exp))
     but1.place(x=300,y=800,width=100,height=70)

     but2=tkinter.Button(text="ない",font=("Meiryo",24),command=lambda: disp_wro(x=exp))
     but2.place(x=1000,y=800,width=100,height=70)

     widgets_but.extend([but1,but2])

    else:
        but1=tkinter.Button(text="ある",font=("Meiryo",24), command=lambda: disp_wro(x=exp))
        but1.place(x=300,y=800,width=100,height=70)
        
        but2=tkinter.Button(text="ない",font=("Meiryo",24),command=lambda: disp_cor(x=exp))
        but2.place(x=1000,y=800,width=100,height=70)
        
        widgets_but.extend([but1,but2])


#ゲーム画面0に戻る
def ret_to_0():
    clear_screen()
    display0()

#中断ボタンの表示
def disp_butex():
    but_ex=tkinter.Button(text="中断",font=("Meiryo",24),command=ret_to_0)
    but_ex.place(x=1200,y=500,width=100,height=70)

    widgets_but.append(but_ex)

def disp_butans():
    but=tkinter.Button(text="答えてもらう",font=("Meiryo",24),command=get_ans)
    but.place(x=600,y=800,width=200,height=70)

    widgets_but.append(but)


def clear_screen():
    global cvs2
    cvs.delete("all")
    if cvs2 is not None:
        cvs2.destroy()
        cvs2=None
    for w in widgets_but:
        w.destroy()
    widgets_but.clear()
    for w in widgets_tex:
        w.destroy()
    widgets_tex.clear()

def disp_cor(x,txt="正解!"):
    cvs.create_rectangle(550,300,850,700,fill="white")
    cvs.create_text(700,350,text=f"{txt}",font=("Meiryo",24))
    but1 = tkinter.Button(text="次の問題へ",font=("Meiryo",24),command=dispB_again)
    but1.place(x=600,y=400,width=200,height=50)

    but2 = tkinter.Button(text="やめる",font=("Meiryo",24),command=ret_to_0)
    but2.place(x=600,y=600,width=200,height=50)

    but3 = tkinter.Button(text="解説を見る",font=("Meiryo",24),command=lambda: show_why(x))
    but3.place(x=600,y=500,width=200,height=50)

    widgets_but.extend([but1,but2,but3])

def show_why(a):
    global cvs2
    cvs2 = tkinter.Canvas(root,width=900,height=200, bg="white")
    cvs2.place(x=250,y=700)
    label1 = tkinter.Label(root,text=f"解説:{a}",font=("Meiryo",24),wraplength=1000)
    label1.place(x=250,y=700)
    widgets_tex.extend([label1])

def dispB_again():
    clear_screen()
    displayB()

def disp_wro(x,txt="不正解..."):
    disp_cor(x,txt)


#game Aに移行
def trans_A():
    clear_screen()
    displayA()

#game Bに移行
def trans_B():
    clear_screen()
    displayB()

#スタート画面の表示
def display0():
    cvs.create_text(700,100,text="AIあるなしクイズ",font=("Meiryo",36))

    but1=tkinter.Button(text="game A",font=("Meiryo",24),command=trans_A) #game Aに移動
    but1.place(x=600,y=300,width=200,height=100)

    but2=tkinter.Button(text="game B",font=("Meiryo",24),command=trans_B) #game Bに移動
    but2.place(x=600,y=500,width=200,height=100)

    but3=tkinter.Button(text="quit",font=("Meiryo",24),command=root.destroy) #ゲーム終了
    but3.place(x=600,y=700,width=200,height=100)

    widgets_but.extend([but1,but2,but3])

    #end

#ゲーム画面Aの表示
def displayA():

    cvs.create_rectangle(300,50,700,750, fill = "deep pink", outline = "red", width=5)
    cvs.create_rectangle(700,50,1100,750, fill = "sky blue", outline = "blue", width=5)

    cvs.create_text(500,100, text="ある", fill="black",font=("Meiryo",36))
    cvs.create_text(900,100, text="ない", fill="black",font=("Meiryo",36))

    for i in range(3):
        disp_text(350,200+i*150)

    for i in range(3):
        disp_text(750,200+i*150)

    for i in range(3):
        cvs.create_rectangle(350,200+i*150,650,300+i*150, fill="white",outline="black")
        cvs.create_rectangle(750,200+i*150,1050,300+i*150, fill="white",outline="black")


    disp_butans()

    disp_butex()

    


    #end

#ゲーム画面Bの表示
def displayB():

    cvs.create_rectangle(300,50,700,750, fill = "deep pink", outline = "red", width=5)
    cvs.create_rectangle(700,50,1100,750, fill = "sky blue", outline = "blue", width=5)

    cvs.create_text(500,100, text="ある", fill="black",font=("Meiryo",36))
    cvs.create_text(900,100, text="ない", fill="black",font=("Meiryo",36))

    for i in range(3):
        cvs.create_rectangle(350,200+i*150,650,300+i*150, fill="white",outline="black")
        cvs.create_rectangle(750,200+i*150,1050,300+i*150, fill="white",outline="black")

    flag=random.choice([True,False])

    ans = get_prob(flag)

    disp_aru(ans[0])
    disp_nai(ans[1])

    
    disp_butex()

    print("ansの型:", type(ans))
    print("ansの内容:", repr(ans))

    disp_but(a=flag, b=ans[2][0],exp=ans[2][1])


    #end

display0()
root.mainloop()