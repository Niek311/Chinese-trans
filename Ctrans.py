import tkinter as tk
from tkinter import Canvas
from tkinter.constants import BOTH
from PIL import Image,ImageTk
from pystray import MenuItem as item
import pystray
import os, sys,re
from ctypes import windll
import sqlite3
from pypinyin.contrib.tone_convert import to_tone
import pyautogui
import datetime
import cv2,pytesseract

windll.shcore.SetProcessDpiAwareness(1)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path,"UI",relative_path)

def changemode(event):
    global switch,toggle
    if event.widget.cget('image') == 'pyimage11':
        try:
            canvas.delete("magsrch")
            canvas.delete("editsrch")
        except:
            pass
        canvas.create_window(36,50,window=ggsrch,tags='ggsrch')
        switch=1
        ggsrch.bind('<Button-1>',lambda event: OCR(root).create_screen_canvas())
    elif event.widget.cget('image') == 'pyimage12':
        switch=2
        try:
            canvas.delete("magsrch")
            canvas.delete("ggsrch")
            Translate.search()
        except:
            pass
        canvas.create_window(36,48,window=editsrch,tags='editsrch')
        editsrch.bind('<Button-1>',Edit.save_to_db)
        
    elif event.widget.cget('image') == 'pyimage13':
        switch=3
        try:
            canvas.delete("editsrch")
            canvas.delete("ggsrch")
            Translate.search()
        except:
            pass
        canvas.create_window(36,50,window=magsrch,tags='magsrch')
    opbox.destroy()
    ggop.destroy()
    editop.destroy()
    magop.destroy()
    toggle=False
          
def on_click2(_):
    global toggle,opbox, ggop, editop, magop
    if toggle is False :
        opbox=tk.Label(canvas,image=imgf,border=0)
        opbox.pack(fill=BOTH,expand=True)
        canvas.create_window(340,14.5,window=opbox)

        ggop=tk.Label(canvas,image=imgg,border=0,bg="#ffffff",cursor='hand2')
        ggop.pack(fill=BOTH,expand=True)
        ggop.bind("<Button-1>",changemode)
        canvas.create_window(315,14.5,window=ggop)


        editop=tk.Label(canvas,image=imgh,border=0,bg="#ffffff",cursor='hand2')
        editop.pack(fill=BOTH,expand=True)
        editop.bind("<Button-1>",changemode)
        canvas.create_window(340,14,window=editop)


        magop=tk.Label(canvas,image=imgi,bg='#ffffff',cursor="hand2")
        magop.pack(fill=BOTH,expand=True)
        magop.bind("<Button-1>",changemode)
        canvas.create_window(365,14.5,window=magop)
        toggle = True
    else:
        if opbox:
            opbox.destroy()
        if ggop:
            ggop.destroy()
        if editop:
            editop.destroy()
        if magop:
            magop.destroy()
        toggle = False

class Win(tk.Tk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        super().iconphoto(True, ImageTk.PhotoImage(file=resource_path("Appicon.png")))
        super().bind("<Button-1>" ,self.clickwin)
        super().bind("<B1-Motion>", self.dragwin)
        super().bind("<Escape>", self.hide_window)

    def quit_window(self,icon, item):
        icon.stop()
        root.destroy()

    def show_window(self,icon, item):
        icon.stop()
        root.after(0,root.deiconify())

    def dragwin(self,event):
        x = super().winfo_pointerx() - self._offsetx
        y = super().winfo_pointery() - self._offsety
        yy=super().winfo_pointery() - super().winfo_rooty()
        if not 80<=yy<=230: 
            super().geometry(f"+{x}+{y}")

    def clickwin(self,event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

    def close_app(self, event):
        self.destroy()

    def hide_window(self,event):
        self.withdraw()
        image=Image.open(resource_path("Appicon.png"))
        menu=(item('Show', self.show_window),item('Quit', self.quit_window),item('Leftclick',self.show_window,default=True,visible=False))
        icon=pystray.Icon("name", image, "Deerfy", menu)
        icon.run()

class Edit():
    def tonechinese(line):
        a=[i+1 for i,x in enumerate(line) if x=='[']
        b=[i for i,x in enumerate(line) if x==']']
        c=[line[a[i]:b[i]] for i in range(len(a))]
        for i in range(len(c)):
            b=list(c[i].split(" "))
            e= ''.join(to_tone(i)+' ' if index != (len(b)-1) else to_tone(i) for index,i in enumerate(b)  )
            f= ''.join((i)+' ' if index != (len(b)-1) else i for index,i in enumerate(b)  )
            line=re.sub(f,e,line)
        return line

    def save_to_db(_):
        gianthe = meaning.get('1.0',meaning.search('[','1.0','end-1c'))
        phonthe = meaning.get(meaning.search('[','1.0','end-1c'),meaning.search(']','1.0','end-1c'))[1:]
        phienam = Edit.tonechinese(meaningkr.get('1.0','end-1c'))
        nghia = meaningvn.get('1.0','end-1c')
        data=(phonthe,gianthe,phienam,nghia)
        c.execute(f"INSERT INTO C_dict VALUES (?,?,?,?);",data)
        conn.commit()
        search_return.configure(state='normal')
        search_return.insert(tk.END," - Change Saved")

    def prevent_delete(event, text_widget):
        selected_text= '`~!@#*^$%#'
        try:
            selected_text = text_widget.selection_get()
        except:
            pass
        try:
            if event.keysym == 'BackSpace' and (
                (text_widget.get(f"{text_widget.index(tk.INSERT)}-1c") == '[' and '[' in selected_text) or
                text_widget.get(f"{text_widget.index(tk.INSERT)}-1c") == ']' or
                text_widget.get(f"{text_widget.index(tk.INSERT)}") == '[' or
                (text_widget.get(f"{text_widget.index(tk.INSERT)}-1c") == '[' and selected_text == '`~!@#*^$%#')
            ):
                return 'break'
            elif event.keysym == 'Delete' and (
                text_widget.get(tk.INSERT) == '[' or
                text_widget.get(tk.INSERT) == ']' 
            ):
                return 'break'
            elif event.keysym and (
                '[' in selected_text or
                ']' in selected_text or
                ' [' in selected_text
            ):
                return 'break'
        except:
            pass

class Menu(tk.Listbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg='white', activestyle='none', cursor='hand2', borderwidth=0,
                         font=('LG Smart UI Regular', 12), width=30, fg='black', highlightbackground="white",
                         highlightcolor="white", selectmode='browse', selectbackground='pink', selectforeground='white',
                         **kwargs)
        self.bind('<KeyPress>', self.key_press2)

    def key_press2(self,_):
        x=entry_search.get()
        if len(_.keysym)==1:
            entry_search.insert(len(x),_.keysym)
            entry_search.focus()
        elif _.keysym=='BackSpace':
            entry_search.delete(len(x)-1,len(x))
            entry_search.focus()
        elif _.keysym=='Return':
            global phien_am,phon_the
            entry_search.delete(0,len(x))
            entry_search.insert(0,menu.get(menu.curselection())[0:(menu.get(menu.curselection()).index('[')-5)])
            phien_am = menu.get(menu.curselection())[(menu.get(menu.curselection()).index('[')):(menu.get(menu.curselection()).index(']')+1)]
            phon_the = menu.get(menu.curselection())[(menu.get(menu.curselection()).index('{')+1):(menu.get(menu.curselection()).index('}'))]
            entry_search.focus()
            Translate.handle_enter("<Return>")
            phien_am=None
            phon_the=None

    def update(self,data):
        # Clear the Combobox
        self.delete(0, tk.END)
        # Add values to the combobox
        for value in data:
            self.insert(tk.END,str(value[0])+'     '+str(value[1])+' '+'{'+str(value[2])+'}')

class EntryBox(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg='white', borderwidth=0, font=('Segoe UI', 12), width=30, fg='#808782', **kwargs)
        self.insert(0, 'Search..')
        self.bind("<FocusIn>", self.handle_focus_in)
        self.bind("<FocusOut>", self.handle_focus_out)
        self.bind("<Return>", Translate.handle_enter)
        self.bind("<KeyRelease>", self.key_release)
        self.bind("<Down>", self.down_key)
    
    def handle_focus_in(self,_):
        if entry_search.get() == 'Search..' :
            entry_search.delete(0, tk.END)
            entry_search.config(fg='#2b2b2b')
    
    def handle_focus_out(self,_):
        if not entry_search.get():
            try:
                entry_search.config(fg='#808782')
                entry_search.insert(0, "Search..")
                search_return.destroy()
                bgr1.destroy()
                bgr2.destroy()
                bgr3.destroy()
                meaning.destroy()
                meaningkr.destroy()
                meaningvn.destroy()
            except:
                pass
          
    def key_release(self,_):
        # print("KeyR",_.keysym,tog)
        Special=["Return","BackSpace", "Control_L","Control_R", "Shift_L","Shift_R", "Alt_L","Alt_R", "Win_L","Command", "Tab", "Caps_Lock", "Delete", "Escape", "Insert", "Home", "End", "Page Up", "Page Down", "Up", "Down", "Left", "Right", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
        x=entry_search.get()
        if menu !='' and _.keysym not in Special and _.keycode <= 229:
            if len(x)>0 and tog==False :
                UI.UIopen()
                menu.pack(pady=85,fill=BOTH,expand=False,padx=20)
                menu.config(height=5)     
                menu.lift()
        
        if x != "" and _.keysym !='Return':
            if switch==3 or switch==2:
                data=[]
                menu.update(sorted(data, key=lambda l: (len(str(l)), str(l))))
                t=c.execute(f"SELECT gian_the,phien_am,phon_the FROM C_dict WHERE gian_the LIKE ('{x}%');").fetchall()
                data.extend(t)
                menu.update(sorted(data, key=lambda l: (len(str(l)), str(l))))
                
        elif x=="":
            UI.UIclose()
            try:
                menu.pack_forget()
                search_return.destroy()
                meaning.destroy()
                meaningkr.destroy()
                meaningvn.destroy()
            except:
                pass
    
    def down_key(self,_):
        if menu.winfo_exists() and not menu.curselection():
            menu.focus()
            menu.select_set(0)

class OCR():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        self.master_screen = tk.Toplevel()
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = tk.Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=True)
        # self.create_screen_canvas()
    
    def take_bounded_screenshot(self,x1, y1, x2, y2):
        image = pyautogui.screenshot(region=(x1, y1, x2, y2))
        file_name = datetime.datetime.now().strftime("%f") + ".png"
        image.save(file_name)
        imagescan=cv2.imread(file_name)
        gray = cv2.cvtColor(imagescan, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        data = pytesseract.image_to_string(blur, lang='eng+chi_sim+chi_tra', config='--psm 6')
        os.remove(file_name)
        return print(data)


    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)
        self.snip_surface.bind("<Button-3>", lambda event :self.exit_screenshot_mode())

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            self.take_bounded_screenshot(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            self.take_bounded_screenshot(self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            self.take_bounded_screenshot(self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            self.take_bounded_screenshot(self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = int(self.snip_surface.canvasx(event.x))
        self.start_y = int(self.snip_surface.canvasy(event.y))
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

class UI():
    def UIopen():
        global bgr1,bgr2,bgr3,tog
        bgr1=tk.Label(canvas,border=0,bg='white',image=imgb)
        bgr1.pack(fill=BOTH,expand=True)
        canvas.create_window(12,63,window=bgr1)

        bgr2=tk.Label(canvas,border=0,bg='white',image=imgc)
        bgr2.pack(fill=BOTH,expand=True)
        canvas.create_window(388,63,window=bgr2)

        bgr3=tk.Label(canvas,border=0,bg='grey',image=imgd)
        bgr3.pack(fill=BOTH,expand=True)
        canvas.create_window(200,150.5,window=bgr3)
        tog=True
        # print('open',tog)
    def UIclose():
        global bgr1,bgr2,bgr3,tog
        bgr1.destroy()
        bgr2.destroy()
        bgr3.destroy()
        tog=False
        # print('close',tog)

class Translate():
    def search():
        menu.pack_forget()
        lookup_value = entry_search.get()
        if switch==3:
            search_return.delete("1.0","end-1c")
            meaning.delete("1.0","end-1c")
            meaningkr.delete("1.0","end-1c")
            meaningvn.delete("1.0","end-1c")
            if lookup_value != "":
                if Translate.vlookup(phien_am, lookup_value) != "Value not found": 
                    result = Translate.vlookup(phien_am, lookup_value)
                    result1 = Translate.vlookup1(phien_am, lookup_value)
                    result2 = Translate.vlookup2(phien_am, lookup_value)
                    
                    search_return.insert(tk.END,"Result for <" + lookup_value + ">")
                    meaning.insert(tk.END,result)
                    meaningkr.insert(tk.END,result1)
                    meaningvn.insert(tk.END,result2)
            
                    canvas.create_window(18, 77, window=search_return, anchor='nw')
                    canvas.create_window(18, 90, window=meaning, anchor='nw')
                    canvas.create_window(18, 120, window=meaningkr, anchor='nw')
                    canvas.create_window(18, 140, window=meaningvn, anchor='nw')
                else:
                    search_return.insert(tk.END,"0 Result for <" + lookup_value + ">")
                    canvas.create_window(18, 80, window=search_return, anchor='nw')
            search_return.configure(state='disabled')
            meaning.configure(state='disabled',background='white')
            meaningkr.configure(state='disabled',background='white')
            meaningvn.configure(state='disabled',background='white')

        elif switch==2:
            search_return.configure(state='normal')
            meaning.configure(state='normal',background='#FFC0CB')
            meaningkr.configure(state='normal',background='#FFC0CB')
            meaningvn.configure(state='normal',background='#FFC0CB')
            search_return.delete("1.0","end-1c")
            meaning.delete("1.0","end-1c")
            meaningkr.delete("1.0","end-1c")
            meaningvn.delete("1.0","end-1c")
            if lookup_value != "":
                if Translate.vlookup(phien_am, lookup_value) != "Value not found": 
                    result = Translate.vlookup(phien_am, lookup_value)
                    result1 = Translate.vlookup1(phien_am, lookup_value)
                    result2 = Translate.vlookup2(phien_am, lookup_value)
                    
                    search_return.insert(tk.END,"Result for <" + lookup_value + ">")
                    meaning.insert(tk.END,result)
                    meaningkr.insert(tk.END,result1)
                    meaningvn.insert(tk.END,result2)
            
                    canvas.create_window(18, 77, window=search_return, anchor='nw')
                    canvas.create_window(18, 90, window=meaning, anchor='nw')
                    canvas.create_window(18, 120, window=meaningkr, anchor='nw')
                    canvas.create_window(18, 140, window=meaningvn, anchor='nw')
                else:
                    search_return.delete("1.0","end-1c")
                    search_return.insert(tk.END,"Add data for <" + lookup_value + ">")
                    canvas.create_window(18, 77, window=search_return, anchor='nw')

                    meaning.insert(tk.END,"Giản-thể [Phồn-thể]" )
                    meaningkr.insert(tk.END,"[Nhập..]" )
                    meaningvn.insert(tk.END,"Nhập.." )

                    meaning.bind('<Key>', lambda event: Edit.prevent_delete(event, meaning))
                    meaningkr.bind('<Key>', lambda event: Edit.prevent_delete(event, meaningkr))

                    canvas.create_window(18, 90, window=meaning, anchor='nw')
                    canvas.create_window(18, 120, window=meaningkr, anchor='nw')
                    canvas.create_window(18, 140, window=meaningvn, anchor='nw')
        elif switch==1:

            search_return.configure(state='normal')
            meaning.configure(state='normal',background='#FFC0CB')
            meaningkr.configure(state='normal',background='#FFC0CB')
            meaningvn.configure(state='normal',background='#FFC0CB')
            search_return.delete("1.0","end-1c")
            meaning.delete("1.0","end-1c")
            meaningkr.delete("1.0","end-1c")
            meaningvn.delete("1.0","end-1c")

    def handle_enter(txt):
        global bgr1,bgr2,bgr3,meaning,meaningkr,meaningvn,search_return
        if entry_search.get() != 'Search..':       

            search_return = tk.Text(canvas,font=('LG Smart Italic', 8), bg='white', fg='#b2b5b0',width=52,height=1,borderwidth=0,undo=True)
            meaning = tk.Text(canvas,font=('LG Smart UI Bold',19), bg='white', fg='#2b2b2b',width=24,height=1,borderwidth=0,undo=True)
            meaningkr = tk.Text(canvas,font=('LG Smart UI Bold',10), bg='white', fg='#2b2b2b',width=45,height=1,borderwidth=0,undo=True)
            meaningvn = tk.Text(canvas,font=('LG Smart UI Bold',10), bg='white', fg='#2b2b2b',width=45,height=5,borderwidth=0,undo=True,wrap='word')
            meaningvn.tag_configure("center", justify='center')
            
            Translate.search()

    def vlookup(phien_am, lookup_value):
        if phien_am is None:
            x=c.execute(f"SELECT phon_the FROM C_dict WHERE gian_the = '{lookup_value}';").fetchone()
        else:
            x=c.execute(f"SELECT phon_the FROM C_dict WHERE gian_the = '{lookup_value}' AND phien_am ='{phien_am}' AND phon_the ='{phon_the}';").fetchone()
        if x != None:
            return f'{lookup_value} [{x[0]}]'
        else:
            return "Value not found"

    def vlookup1(phien_am, lookup_value):
        if phien_am is None:
            x=c.execute(f"SELECT phien_am FROM C_dict WHERE gian_the = '{lookup_value}';").fetchone()
        else:
            x=c.execute(f"SELECT phien_am FROM C_dict WHERE gian_the = '{lookup_value}' AND phien_am ='{phien_am}' AND phon_the ='{phon_the}';").fetchone()
        if x != None:
            return f'{x[0]}'
        else:
            return None

    def vlookup2(phien_am, lookup_value):
        if phien_am is None:
            x=c.execute(f"SELECT nghia FROM C_dict WHERE gian_the = '{lookup_value}';").fetchone()
        else:
            x=c.execute(f"SELECT nghia FROM C_dict WHERE gian_the = '{lookup_value}' AND phien_am ='{phien_am}' AND phon_the ='{phon_the}';").fetchone()
        if x != None:
            return f'{x[0]}'
        else:
            return None

if __name__ == "__main__":
    #Database access
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    #Create root
    root = Win()
    root.title('Deerfy')
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',True)
    root.geometry("400x270+760+275")
    root.attributes("-transparentcolor", "#FAE2E2")
    canvas = Canvas(root, bg="#FAE2E2", highlightthickness=0)
    canvas.pack(fill=BOTH, expand=1)
    # Create bar search
    imga= ImageTk.PhotoImage(Image.open(resource_path("kl.png")))
    bgr=tk.Label(canvas,border=0,image=imga)
    bgr.pack(fill=BOTH,expand=True)
    canvas.create_window(200,50,window=bgr)
    # EntryBox create
    entry_search = EntryBox(canvas)
    canvas.create_window(200,50,window=entry_search)
    # Result drop-down
    menu= Menu(canvas)
    # Image scan mode switch
    imgg1= ImageTk.PhotoImage(Image.open(resource_path("kl6.png")))
    ggsrch=tk.Label(canvas,image=imgg1,bg='white',cursor="hand2")
    # Edit/save mode switch
    imgh1= ImageTk.PhotoImage(Image.open(resource_path("kl5.png")))
    editsrch=tk.Label(canvas,image=imgh1,bg='white',cursor="hand2")
    # Search mode switch
    imgi1= ImageTk.PhotoImage(Image.open(resource_path("kl1.png")))
    magsrch=tk.Label(canvas,image=imgi1,bg='white',cursor="hand2")
    magsrch.bind('<Button-1>', Translate.handle_enter)
    canvas.create_window(36,50,window=magsrch,tags='magsrch')
    # Meatball button
    imge= ImageTk.PhotoImage(Image.open(resource_path("kl7.png")))
    meatball=tk.Label(canvas,image=imge,bg='white',cursor="hand2")
    meatball.bind('<Button-1>',on_click2)
    canvas.create_window(364,49,window=meatball)
    # Other UI
    imgb= ImageTk.PhotoImage(Image.open(resource_path("kl2.png")))
    imgc= ImageTk.PhotoImage(Image.open(resource_path("kl3.png")))
    imgd= ImageTk.PhotoImage(Image.open(resource_path("kl4.png")))
    imgf= ImageTk.PhotoImage(Image.open(resource_path("kl8.png")))
    imgg= ImageTk.PhotoImage(Image.open(resource_path("kl6.png")).resize((15,15)))
    imgh= ImageTk.PhotoImage(Image.open(resource_path("kl5.png")).resize((15,15)))
    imgi= ImageTk.PhotoImage(Image.open(resource_path("kl1.png")).resize((15,13)))
    # Variable
    tog,toggle = False,False
    opbox, ggop, editop, magop = None, None, None, None 
    switch=3
    phien_am=None
    # Start
    root.mainloop()
# pyinstaller --windowed --onefile --icon=Appicon1.png --add-data="Appicon1.png;." --add-data="Appicon.png;." --add-data="kl.png;." --add-data="kl1.png;." --add-data="kl2.png;." --add-data="kl3.png;." --add-data="kl4.png;." Deerfy.py