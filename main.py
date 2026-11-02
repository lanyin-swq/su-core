from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import threading

from engine import PureCoreEngine

class ChatScreen(Screen):
    """聊天列表页面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Messages", size_hint_y=0.1, font_size='20sp', bold=True))
        
        self.chat_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_list.bind(minimum_height=self.chat_list.setter('height'))
        
        scroll = ScrollView()
        scroll.add_widget(self.chat_list)
        layout.add_widget(scroll)
        
        # 纯净版：初始为空，等待用户在“添加ID”页面创建
        layout.add_widget(Label(text="(No IDs found. Please add an ID.)", size_hint_y=0.8))
        self.add_widget(layout)

class AddIDScreen(Screen):
    """添加ID页面（空白槽位）"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        layout.add_widget(Label(text="Create New ID", size_hint_y=0.2, font_size='20sp', bold=True))
        
        self.id_input = TextInput(hint_text="ID Name", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.id_input)
        
        self.prompt_input = TextInput(hint_text="Initial Memory / System Prompt", multiline=True, size_hint_y=None, height=150)
        layout.add_widget(self.prompt_input)
        
        create_btn = Button(text="Create", size_hint_y=None, height=50)
        create_btn.bind(on_press=self.create_id)
        layout.add_widget(create_btn)
        
        self.status_label = Label(text="", size_hint_y=0.2)
        layout.add_widget(self.status_label)
        
        layout.add_widget(Label()) 
        self.add_widget(layout)

    def create_id(self, instance):
        name = self.id_input.text.strip()
        if name:
            self.status_label.text = f"ID [{name}] Created. Memory slot allocated."
            self.id_input.text = ""
            self.prompt_input.text = ""
        else:
            self.status_label.text = "ID Name cannot be empty."

class BottomNav(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.1
        self.orientation = 'horizontal'
        self.sm = screen_manager
        
        btn_chat = Button(text="Chats", background_color=(0.1, 0.7, 0.1, 1))
        btn_chat.bind(on_press=lambda x: self.switch_tab('chat'))
        self.add_widget(btn_chat)
        
        btn_add = Button(text="Add ID", background_color=(0.3, 0.3, 0.3, 1))
        btn_add.bind(on_press=lambda x: self.switch_tab('add'))
        self.add_widget(btn_add)

    def switch_tab(self, tab_name):
        self.sm.current = tab_name

class SuApp(App):
    def build(self):
        # 初始化底层引擎
        self.engine = PureCoreEngine()
        threading.Thread(target=self.engine.background_loop, daemon=True).start()

        root = BoxLayout(orientation='vertical')
        self.sm = ScreenManager()
        
        self.sm.add_widget(ChatScreen(name='chat'))
        self.sm.add_widget(AddIDScreen(name='add'))
        
        root.add_widget(self.sm)
        root.add_widget(BottomNav(self.sm))
        
        return root

if __name__ == '__main__':
    SuApp().run()
