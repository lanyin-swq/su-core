from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading

from engine import PureCoreEngine

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # 初始化引擎
        self.engine = PureCoreEngine(current_id="su")
        threading.Thread(target=self.engine.background_loop, daemon=True).start()
        
        self.content = BoxLayout()
        self.add_widget(self.content)
        
        # 底部导航栏
        nav = BoxLayout(size_hint_y=0.15)
        btn_chat = Button(text="Chats", background_color=(0.1, 0.7, 0.1, 1))
        btn_chat.bind(on_press=self.show_chat)
        btn_add = Button(text="Add ID", background_color=(0.3, 0.3, 0.3, 1))
        btn_add.bind(on_press=self.show_add)
        nav.add_widget(btn_chat)
        nav.add_widget(btn_add)
        self.add_widget(nav)
        
        self.show_chat(None)

    def show_chat(self, instance):
        self.content.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)
        
        self.chat_log = Label(text="[Contact: Su]\n(Waiting for 8B Brain...)\n", size_hint_y=None, halign='left', valign='top')
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        
        scroll = ScrollView()
        scroll.add_widget(self.chat_log)
        layout.add_widget(scroll)
        
        input_box = BoxLayout(size_hint_y=0.1)
        self.msg_input = TextInput(hint_text="Type here...", multiline=False)
        send_btn = Button(text="Send", size_hint_x=0.2, on_press=self.send_msg)
        input_box.add_widget(self.msg_input)
        input_box.add_widget(send_btn)
        
        layout.add_widget(input_box)
        self.content.add_widget(layout)

    def send_msg(self, instance):
        text = self.msg_input.text
        if text:
            self.chat_log.text += f"\nYou: {text}\nSu: (Thinking...)"
            self.msg_input.text = ""
            
            # 多线程处理，防止 UI 卡死
            def process_thread():
                reply = self.engine.process_user_input(text)
                # 回到主线程更新 UI
                Clock.schedule_once(lambda dt: self.update_ui(reply))
                
            threading.Thread(target=process_thread).start()

    def update_ui(self, reply):
        self.chat_log.text += f"\rSu: {reply}\n"

    def show_add(self, instance):
        self.content.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Create New ID", size_hint_y=0.2))
        self.name_input = TextInput(hint_text="ID Name", multiline=False, size_hint_y=0.2)
        layout.add_widget(self.name_input)
        layout.add_widget(Button(text="Confirm", size_hint_y=0.2, on_press=self.do_create))
        self.content.add_widget(layout)

    def do_create(self, instance):
        self.show_chat(None)

class SuApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    SuApp().run()
