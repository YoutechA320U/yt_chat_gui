import asyncio
from io import BytesIO
from PIL import Image
import PySimpleGUI as sg
sg.theme("Reddit")

def image_to_data(im):

    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

def make_background(window, file, main_frame):

    global images

    def find_frames(widget):
        widgets = list(widget.children.values())
        if isinstance(widget, (sg.tk.Frame, sg.tk.LabelFrame)):
            widget.update()
            x, y = widget.winfo_rootx() - x0, widget.winfo_rooty() - y0
            width, height = widget.winfo_width(), widget.winfo_height()
            new_im = im_.crop((x, y, x+width, y+height))
            image = sg.tk.PhotoImage(data=image_to_data(new_im))
            images.append(image)
            label = sg.tk.Label(widget, image=image, padx=0, pady=0, bd=0, bg=bg)
            label.place(x=0, y=0)
            label.lower()
        for widget in widgets:
            find_frames(widget)

    size = window.size
    im_ = Image.open(file).resize(size)
    root = window.TKroot
    widgets = list(root.children.values())
    x0, y0 = root.winfo_rootx(), root.winfo_rooty()

    frame = sg.tk.Frame(root, padx=0, pady=0, bd=0, bg=bg)
    frame.place(x=0, y=0)
    images = []
    image = sg.tk.PhotoImage(data=image_to_data(im_))
    images.append(image)
    label = sg.tk.Label(frame, image=image, padx=0, pady=0, bd=0, bg=bg)
    label.pack()
    main_frame.Widget.master.place(in_=frame, anchor='center', relx=.5, rely=.5)
    frame.lower()
    frame.update()
    for widget in widgets:
        find_frames(widget)
        
bg = sg.theme_background_color()
background_image_file = 'img_data/bg.png'
w, h = size = 500, 500  # size of background image

sg.set_options(dpi_awareness=True)

frame = [
         [sg.Image(filename = 'img_data/chara1.png', pad=((0,0),(0,100)), key='chara'),sg.Multiline(size=(46, 19.4), pad=((0,0),(0,0)), key='-OUT-', disabled=True, enable_events=True)],
         [sg.Multiline(size=(40, 6), pad=((0,0),(0,0)),key='-IN-', enter_submits=False)],
         [sg.Button('send',size=(10, 2), bind_return_key=True), sg.Button('exit', size=(10, 2))]
         ]
         
layout=[[sg.Frame('',frame, size=(500, 500), border_width=0, key='FRAME')]]
location = sg.Window.get_screen_size()

window = sg.Window('yt_chat_gui', layout, size=(500, 500),finalize=True)
images = []
make_background(window, background_image_file, window['FRAME'])


task1= ""
task2= ""
task3= ""
response = ""
reslist = ""
question = ""  
reslen = 0
reswait= 0
msgwaitflag= 0
async def anime():
    global window, response, question, reslist, reslen, reswait, msgwaitflag
    while True:
     await asyncio.sleep(0.05)
     if (reslist !="" and reslist[reslen-1] !="。" and reslist[reslen-1] !="\n" and reslist[reslen-1] !="、"):
        event, values = window.read(timeout=3)
        window['chara'].Update(filename = 'img_data/chara2.png')
        await asyncio.sleep(0.05)
        event, values = window.read(timeout=3)
        window['chara'].Update(filename = 'img_data/chara1.png')
        await asyncio.sleep(0.05)
        event, values = window.read(timeout=3)
     waitmsg_no = 1
     while reswait == 1 and reslist =="" :
        msgwaitflag= 1
        if waitmsg_no == 1:
           await asyncio.sleep(0.3)
           event, values = window.read(timeout=3)
           window['-OUT-'].update('')
           window['-OUT-'].print("回答を生成中です", end="")
        if waitmsg_no != 0 and waitmsg_no != 5:  
           await asyncio.sleep(0.3) 
           event, values = window.read(timeout=3)
           window['-OUT-'].print(".", end="")
        if waitmsg_no == 5:   
           await asyncio.sleep(0.3) 
           waitmsg_no = 0
        waitmsg_no += 1
     msgwaitflag= 0
     if task3.done() == True or task2.done() == True:
        break

    

async def bing():
    global response, question, reslist
    while True:
     await asyncio.sleep(0.01)
     if question !="" and response =="":
        response = "ここには入力に対する出力データが表示されます。\nテスト、テストです。\n\n本日は晴天なり。"
        reslist = list(response)
        #print(reslist)
        reslen < len(reslist)
     if task3.done() == True or task1.done() == True:
        break



async def box():    
    global response, question, reslen, reslist, reswait, msgwaitflag
    while True:
      await asyncio.sleep(0.01)
      event, values = window.read(timeout=3)
      if (event == 'send') and reswait == 0:
         window['-OUT-'].update('')
         question = values['-IN-']
         if question != "":
            reswait = 1
      if reswait == 1 and response !="" and  msgwaitflag==0:
         event, values = window.read(timeout=3)
         window['-OUT-'].update('')
         while reslen < len(reslist):
          await asyncio.sleep(0.01)
          event, values = window.read(timeout=3)
          if (reslist[reslen-1] =="。" or reslist[reslen-1] =="\n" or reslist[reslen-1] =="、"):
             await asyncio.sleep(0.5)
          else:
             await asyncio.sleep(0.01)
          if event in (sg.WIN_CLOSED, 'exit'):
              break  
          window['-OUT-'].print(reslist[reslen], end="")
          reslen += 1
         if reslen > 0 and reslen >= len(reslist):
          window['-IN-'].update('')
          question = "" 
          response =""
          reslist =""
          reswait = 0
          reslen =0

         
      if event in (sg.WIN_CLOSED, 'exit'):
         window.close()
         break     
      if task1.done() == True or task2.done() == True:
         pass
         break

async def main():
    global task1, task2 ,task3
    task1 = asyncio.create_task(bing())
    task2 = asyncio.create_task(anime())
    task3 = asyncio.create_task(box())
    await task1
    await task2
    await task3

if __name__ == "__main__":
    asyncio.run(main())

