#!/usr/bin/env python
# coding: utf-8

# ##  ライブラリのインポート
# 

# In[1]:


# -*- coding:utf-8 -*-
import tkinter
import tkinter.filedialog as tf
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ## Modelクラス
# ### 画像を扱うクラス

# In[2]:


class Model():
    # 画像処理前か画像処理後かを指定
    BEFORE = 1
    AFTER = 2
 

    def __init__(self):

        # PIL画像オブジェクトを参照
        self.before_image = None
        self.after_image = None

        # Tkinter画像オブジェクトを参照
        self.before_image_tk = None
        self.after_image_tk = None

    def get_image(self, type):
        'Tkinter画像オブジェクトを取得する'

        if type == Model.BEFORE:
            if self.before_image is not None:
                # Tkinter画像オブジェクトに変換
                self.before_image_tk = ImageTk.PhotoImage(self.before_image)
            return self.before_image_tk

        elif type == Model.AFTER:
            if self.after_image is not None:
                # Tkinter画像オブジェクトに変換
                self.after_image_tk = ImageTk.PhotoImage(self.after_image)
            return self.after_image_tk

        else:
            return None

    def read(self, path):
        '画像の読み込みを行う'
        
        #読み込んだファイルパスがCSVの時の処理
        if path.endswith('.csv'):
            print("CSVファイルを読み込みました。")
            #CSVファイルを読み込む
            #path = np.loadtxt(path,delimiter=",")
            path = np.genfromtxt(path,encoding="utf-8_sig",delimiter=",")
            #img = Image.fromarray(path)
            fig = plt.figure()
            #ax =self.fig.add_subplot()
            #ax = img
            plt.imshow(path, aspect="auto", interpolation = "none")
            #plt.colorbar()
            plt.show()
            # グラフをファイルに保存する
            fig.savefig("imgPIL.png")
            #保存した画像を呼び出す
            self.before_image = Image.open("./imgPIL.png")
            
            #PILフォーマットへ変換
            #self.before_image = Image.fromarray(imp)
            #self.before_image = self.before_image.convert("L")
                
            print("---元サイズ---")
            print("width:",self.before_image.width)
            print("height:",self.before_image.height,'\n')
            #self.before_imageを400*400に合うようにリサイズする。
            self.before_image = self.before_image.resize(( int(self.before_image.width * (530/self.before_image.width)), 
                                                   int(self.before_image.height * (530/self.before_image.height)) ))

        
        #読み込んだファイルパスがCSV以外(png等の画像)のファイルの処理
        else:
            # pathの画像を読み込んでPIL画像オブジェクト生成
            self.before_image = Image.open(path)
            print("---元サイズ---")
            print("width:",self.before_image.width)
            print("height:",self.before_image.height,'\n')
            #self.before_imageを400*400に合うようにリサイズする。
            self.before_image = self.before_image.resize(( int(self.before_image.width * (400/self.before_image.width)), 
                                                   int(self.before_image.height * (400/self.before_image.height)) ))
        
    def round(self, value, min, max):
        'valueをminからmaxの範囲に丸める'

        ret = value
        if (value < min):
            ret = min
        if (value > max):
            ret = max

        return ret

    def crop(self, param):
        '画像をクロップ'

        if len(param) != 4:
            return
        if self.before_image is None:
            return

        print(param)
        # 画像上の選択範囲を取得（x1,y1）-（x2,y2）
        x1, y1, x2, y2 = param

        # 画像外の選択範囲を画像内に切り詰める
        x1 = self.round(x1, 0, self.before_image.width)
        x2 = self.round(x2, 0, self.before_image.width)
        y1 = self.round(y1, 0, self.before_image.height)
        y2 = self.round(y2, 0, self.before_image.height)

        # x1 <= x2 になるように座標を調節
        if x1 <= x2:
            crop_x1 = x1
            crop_x2 = x2
        else:
            crop_x1 = x2
            crop_x2 = x1

        # y1 <= y2 になるように座標を調節
        if y1 <= y2:
            crop_y1 = y1
            crop_y2 = y2
        else:
            crop_y1 = y2
            crop_y2 = y1

        # PIL Imageのcropを実行
        self.after_image = self.before_image.crop(
            (
                crop_x1,
                crop_y1,
                crop_x2,
                crop_y2
            )
        )
        
        a_crop_x1 = (crop_x1* 530/self.before_image.width)
        a_crop_x2 = (crop_x2* 530/self.before_image.width)
            
        a_crop_y1 = (crop_y1* 530/self.before_image.height)    
        a_crop_y2 = (crop_y2* 530/self.before_image.height) 
        
        
        #print("---トリミング座標(元座標)---","\n")
       # print("(",a_crop_x1,",",a_crop_y1,",",a_crop_x2,",",a_crop_y2,")")


# ## Viewクラス
# ### UIを扱うクラス

# In[3]:


class View():
    # キャンバス指定用
    LEFT_CANVAS = 1
    RIGHT_CANVAS = 2

    def __init__(self, app, model):

        self.master = app
        self.model = model

        # アプリ内のウィジェットを作成
        self.create_widgets()

    def create_widgets(self):
        'アプリ内にウィジェットを作成・配置する'

        # キャンバスのサイズ
        canvas_width = 400
        canvas_height = 400

        # キャンバスとボタンを配置するフレームの作成と配置
        self.main_frame = tkinter.Frame(
            self.master
        )
        self.main_frame.pack()

        # ラベルを配置するフレームの作成と配置
        self.sub_frame = tkinter.Frame(
            self.master
        )
        self.sub_frame.pack()

        # キャンバスを配置するフレームの作成と配置
        self.canvas_frame = tkinter.Frame(
            self.main_frame
        )
        self.canvas_frame.grid(column=1, row=1)

        # ボタンを８位するフレームの作成と配置
        self.button_frame = tkinter.Frame(
            self.main_frame
        )
        self.button_frame.grid(column=2, row=1)

        # １つ目のキャンバスの作成と配置
        self.left_canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="gray",
        )
        self.left_canvas.grid(column=1, row=1)

        # ２つ目のキャンバスの作成と配置
        self.right_canvas = tkinter.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="gray",
        )
        self.right_canvas.grid(column=2, row=1)

        # ファイル読み込みボタンの作成と配置
        self.load_button = tkinter.Button(
            self.button_frame,
            text="ファイル選択"
        )
        self.load_button.pack()
        
        #セーブボタンの作成と配置
        self.save_button = tkinter.Button(
            self.button_frame,
            text="保存"
        )
        self.save_button.pack()

        # メッセージ表示ラベルの作成と配置

        # メッセージ更新用
        self.message = tkinter.StringVar()

        self.message_label = tkinter.Label(
            self.sub_frame,
            textvariable=self.message
        )
        self.message_label.pack()

    def draw_image(self, type):
        '画像をキャンバスに描画'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
            image = self.model.get_image(Model.BEFORE)
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
            image = self.model.get_image(Model.AFTER)
        else:
            return

        if image is not None:
            # キャンバス上の画像の左上座標を決定
            sx = (canvas.winfo_width() - image.width()) // 2
            sy = (canvas.winfo_height() - image.height()) // 2

            # キャンバスに描画済みの画像を削除
            objs = canvas.find_withtag("image")
            for obj in objs:
                canvas.delete(obj)

            # 画像をキャンバスの真ん中に描画
            canvas.create_image(
                sx, sy,
                image=image,
                anchor=tkinter.NW,
                tag="image"
            )
        
            #canvas.create_image(200-(self.controller.w*(400/self.controller.h)/2), 0, image=img, anchor=tkinter.NW)

    def draw_selection(self, selection, type):
        '選択範囲を描画'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
        else:
            return

        # 一旦描画済みの選択範囲を削除
        self.delete_selection(type)

        if selection:
            # 選択範囲を長方形で描画
            canvas.create_rectangle(
                selection[0],
                selection[1],
                selection[2],
                selection[3],
                outline="red",
                width=3,
                tag="selection_rectangle"
            )

    def delete_selection(self, type):
        '選択範囲表示用オブジェクトを削除する'

        # typeに応じて描画先キャンバスを決定
        if type == View.LEFT_CANVAS:
            canvas = self.left_canvas
        elif type == View.RIGHT_CANVAS:
            canvas = self.right_canvas
        else:
            return

        # キャンバスに描画済みの選択範囲を削除
        objs = canvas.find_withtag("selection_rectangle")
        for obj in objs:
            canvas.delete(obj)

    def draw_message(self, message):
        self.message.set(message)

    def select_file(self):
        'ファイル選択画面を表示'

        # ファイル選択ダイアログを表示
        file_path = tkinter.filedialog.askopenfilename(
            filetypes=[('data files','*.csv;*.png')],
            initialdir="."
        )
        
        #読み込んだファイルがcsvファイルだった時の処理
        #if file_path.endswith('.csv'):
                #file_path = np.loadtxt("file_path", delimiter=",")
        return file_path


# ## Controllerクラス
# ### クラスはユーザーからの入力を受け付け、Model と View の制御を行うクラス

# In[4]:


class Controller():
    INTERVAL = 50

    def __init__(self, app, model, view):
        self.master = app
        self.model = model
        self.view = view

        # マウスボタン管理用
        self.pressing = False
        self.selection = None

        # ラベル表示メッセージ管理用
        self.message = "ファイルを読み込んでください"

        self.set_events()

    def set_events(self):
        '受け付けるイベントを設定する'

        # キャンバス上のマウス押し下げ開始イベント受付
        self.view.left_canvas.bind(
            "<ButtonPress>",
            self.button_press
        )

        # キャンバス上のマウス動作イベント受付
        self.view.left_canvas.bind(
            "<Motion>",
            self.mouse_motion,
        )

        # キャンバス上のマウス押し下げ終了イベント受付
        self.view.left_canvas.bind(
            "<ButtonRelease>",
            self.button_release,
        )

        # 読み込みボタン押し下げイベント受付
        self.view.load_button['command'] = self.push_load_button
        
        # 保存ボタン押し下げイベント受付
        self.view.save_button['command'] = self.push_save_button

        # 画像の描画用のタイマーセット
        self.master.after(Controller.INTERVAL, self.timer)

    def timer(self):
        '一定間隔で画像等を描画'

        # 画像処理前の画像を左側のキャンバスに描画
        self.view.draw_image(
            View.LEFT_CANVAS
        )

        # 画像処理後の画像を右側のキャンバスに描画
        self.view.draw_image(
            View.RIGHT_CANVAS
        )

        # トリミング選択範囲を左側のキャンバスに描画
        self.view.draw_selection(
            self.selection,
            View.LEFT_CANVAS
        )

        # ラベルにメッセージを描画
        self.view.draw_message(
            self.message
        )

        # 再度タイマー設定
        self.master.after(Controller.INTERVAL, self.timer)

    def push_load_button(self):
        'ファイル選択ボタンが押された時の処理'

        # ファイル選択画面表示
        file_path = self.view.select_file()
       
        # 画像ファイルの読み込みと描画
        if len(file_path) != 0:
            self.model.read(file_path)

        self.selection = None

        # 選択範囲を表示するオブジェクトを削除
        self.view.delete_selection(view.LEFT_CANVAS)
        
        #self.extensionは、読み込んだファイルパスがcsvだったら
        #TrueをCSV以外のファイルだとFalseを格納している。
        self.extension = file_path.endswith(".csv")
        
        #CSVファイル以外のときの処理
        if self.extension != 1:
            #圧縮後の縦と横の大きさをwとhに格納する
            self.w,self.h = self.model.before_image.size
            
            print("---圧縮後---")
            print('width:',self.w)
            print('height:',self.h,'\n')
        #圧縮後の縦と横の大きさをwとhに格納する
        self.w,self.h = self.model.before_image.size
            
        print("---圧縮後---")
        print('width:',self.w)
        print('height:',self.h,'\n')
            
        # メッセージを更新
        self.message = "トリミングする範囲を指定してください"
        
    def push_save_button(self):
        '保存ボタンが押された時の処理'
        
        im = model.after_image
        
        #ダイアログでの保存時の拡張子選択設定
        typ = [('data files','*.csv;*.png')] 
        
        #保存先のパスをダイアログで指定できるようにする
        save_path = tf.asksaveasfilename(filetypes = typ)

        #保存時のパスがcsvファイルかどうか
        self.extension_save = save_path.endswith(".csv")
        
        #CSVファイルの時、トリミング後の画像をnumpyarryで行列化する。
        if self.extension_save == 1:
            #after_imageをcsv形式で保存する為のグレースケール化
            im = im.convert("L")
            im = np.array(im)
            np.savetxt(save_path,im,delimiter=",")
            
        #CSV以外のとき
        else :
           # Modelクラスのafter_image←トリミング後の画像を
           # 先程の指定したパスで保存する。
        
            self.extension_con = save_path.endswith(".png")
            
            #PNGのとき
            if self.extension_con == 1:
                im = im.convert("RGBA")
            
            #JPGのとき
            else :
                im = im.convert("RGB")
    
            im.save(save_path)
        
        
    def button_press(self, event):
        'マウスボタン押し下げ開始時の処理'

        # マウスクリック中に設定
        self.pressing = True

        self.selection = None

        # 現在のマウスでの選択範囲を設定
        self.selection = [
            event.x,
            event.y,
            event.x,
            event.y
        ]

        # 選択範囲を表示するオブジェクトを削除
        self.view.delete_selection(View.LEFT_CANVAS)

    def mouse_motion(self, event):
        'マウスボタン移動時の処理'

        if self.pressing:
            # マウスでの選択範囲を更新
            self.selection[2] = event.x
            self.selection[3] = event.y

    def button_release(self, event):
        'マウスボタン押し下げ終了時の処理'
        

        if self.pressing:

            # マウスボタン押し下げ終了
            self.pressing = False

            # マウスでの選択範囲を更新
            self.selection[2] = event.x
            self.selection[3] = event.y

            # 画像の描画位置を取得
            objs = self.view.left_canvas.find_withtag("image")
            if len(objs) != 0:
                draw_coord = self.view.left_canvas.coords(objs[0])

                # 選択範囲をキャンバス上の座標から画像上の座標に変換
                x1 = self.selection[0] - draw_coord[0]
                y1 = self.selection[1] - draw_coord[1]
                x2 = self.selection[2] - draw_coord[0]
                y2 = self.selection[3] - draw_coord[1]

                # 画像をcropでトリミング
               
                print("---トリミング座標(圧縮後の座標)---")
                self.model.crop(
                   (int(x1), int(y1), int(x2), int(y2))
                )
                print("\n")
                # メッセージを更新
                self.message = "トリミングしました！"


# ## main
# ### アプリの実行を行う

# In[7]:


app = tkinter.Tk()

# アプリのウィンドウのサイズ設定
app.geometry("1000x430")
app.title("トリミングアプリ")

model = Model()
view = View(app, model)
controller = Controller(app, model, view)

app.mainloop()


# In[ ]:





# In[ ]:




