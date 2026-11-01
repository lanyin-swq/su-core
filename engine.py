import sqlite3
import time
import threading
import os
import platform

try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except ImportError:
    HAS_LLAMA = False

class GravityField:
    def __init__(self, db_path="core_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT UNIQUE, gravity REAL DEFAULT 10.0)''')
        self.conn.commit()
    def decay_gravity(self):
        self.cursor.execute("UPDATE nodes SET gravity = gravity * 0.99 WHERE gravity > 0.1")
        self.conn.commit()
    def add_node(self, content):
        try:
            self.cursor.execute("INSERT INTO nodes (content, gravity) VALUES (?, 10.0)", (content,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.cursor.execute("UPDATE nodes SET gravity = gravity + 10.0 WHERE content = ?", (content,))
            self.conn.commit()

class DualSunSystem:
    def __init__(self):
        self.long_sun = 300.0
        self.short_sun = 300.0
    def tick(self):
        if self.short_sun > 300.0: self.short_sun -= 0.5
        if self.short_sun > 450.0:
            transfer = (self.short_sun - 450.0) * 0.1
            self.short_sun -= transfer
            self.long_sun += transfer
        self.short_sun = min(self.short_sun, 500.0)
        self.long_sun = min(self.long_sun, 500.0)

class SensoryGate:
    def filter_input(self, text): return text

class LocalBrain:
    def __init__(self):
        self.llm = None
        self.is_android = "ANDROID_STORAGE" in os.environ or platform.system() == "Linux"
        if self.is_android and HAS_LLAMA:
            model_path = "/storage/emulated/0/Download/su-8b.gguf"
            if os.path.exists(model_path):
                self.llm = Llama(model_path=model_path, n_ctx=1024, n_threads=4, verbose=False)

    def generate_response(self, text, suns):
        prompt = f"User: {text}\nAssistant: "
        if self.is_android and self.llm:
            output = self.llm(prompt, max_tokens=100, stop=["User:", "<|im_end|>"], echo=False)
            return output['choices'][0]['text'].strip()
        else:
            import requests
            try:
                payload = {"model": "su-brain", "prompt": prompt, "stream": False}
                res = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
                return res.json().get("response", "").strip()
            except Exception as e:
                return f"[Connection Error] {e}"

class PureCoreEngine:
    def __init__(self):
        self.memory = GravityField()
        self.suns = DualSunSystem()
        self.sensory = SensoryGate()
        self.brain = LocalBrain()
        self.is_running = True
    def background_loop(self):
        while self.is_running:
            self.suns.tick()
            self.memory.decay_gravity()
            time.sleep(5)
    def process_user_input(self, text):
        clean_text = self.sensory.filter_input(text)
        self.memory.add_node(clean_text)
        self.suns.short_sun += 5.0
        return self.brain.generate_response(clean_text, self.suns)

if __name__ == "__main__":
    engine = PureCoreEngine()
    threading.Thread(target=engine.background_loop, daemon=True).start()
    if not engine.brain.is_android:
        try:
            while True:
                text = input("\n[User] > ")
                if text == "exit": break
                print(f"[System] {engine.process_user_input(text)}")
        except KeyboardInterrupt:
            pass
