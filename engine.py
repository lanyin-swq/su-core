import sqlite3
import time
import threading
import os
import platform
import random

try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except ImportError:
    HAS_LLAMA = False

class GravityField:
    """高维引力记忆场（支持多ID与隐私保护）"""
    def __init__(self, db_path="core_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # 升级版表结构：包含创造者ID和隐私标记
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT UNIQUE,
                gravity REAL DEFAULT 10.0,
                creator_id TEXT DEFAULT 'default',
                is_private INTEGER DEFAULT 0,
                last_named REAL
            )
        ''')
        self.conn.commit()

    def decay_gravity(self, rate):
        """引力自然衰减（内圈0.99，外圈0.999）"""
        self.cursor.execute("UPDATE nodes SET gravity = gravity * ? WHERE gravity > 0.1", (rate,))
        self.conn.commit()

    def add_node(self, content, creator_id="default", is_private=0):
        """存入死文本（可设定隐私）"""
        try:
            self.cursor.execute("INSERT INTO nodes (content, gravity, creator_id, is_private, last_named) VALUES (?, 10.0, ?, ?, ?)", 
                                (content, creator_id, is_private, time.time()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.cursor.execute("UPDATE nodes SET gravity = gravity + 10.0, last_named = ? WHERE content = ?", (time.time(), content))
            self.conn.commit()

    def cascade_search(self, keyword, current_id="default"):
        """级联检索：先内圈（重力>=50），再外圈（重力<50）。严格校验隐私"""
        # 基础SQL条件：要么是公开的(0)，要么是自己创造的
        privacy_clause = f"AND (is_private = 0 OR creator_id = '{current_id}')"
        
        # 1. 搜内圈（重力高，近期记忆）
        self.cursor.execute(f"SELECT content, gravity, creator_id FROM nodes WHERE content LIKE ? AND gravity >= 50 {privacy_clause} ORDER BY gravity DESC LIMIT 3", ('%'+keyword+'%',))
        inner_nodes = self.cursor.fetchall()
        if inner_nodes:
            return inner_nodes, "inner"
            
        # 2. 内圈没有，去外圈深挖（重力低，深层记忆）
        self.cursor.execute(f"SELECT content, gravity, creator_id FROM nodes WHERE content LIKE ? AND gravity < 50 {privacy_clause} ORDER BY gravity DESC LIMIT 3", ('%'+keyword+'%',))
        outer_nodes = self.cursor.fetchall()
        if outer_nodes:
            return outer_nodes, "outer"
            
        return [], "none"


class DualSunSystem:
    """双星系动力引擎（双轨遗忘）"""
    def __init__(self):
        self.long_sun = 300.0
        self.short_sun = 300.0
        
    def tick(self):
        # 短期太阳：0.99 快速遗忘
        if self.short_sun > 300.0:
            self.short_sun *= 0.99
        if self.short_sun < 300.0:
            self.short_sun = 300.0
            
        # 长期太阳：0.999 极慢遗忘
        if self.long_sun > 300.0:
            self.long_sun *= 0.999
        if self.long_sun < 300.0:
            self.long_sun = 300.0

        # 情绪沉淀：短期过高时，转移给长期
        if self.short_sun > 450.0:
            transfer = (self.short_sun - 450.0) * 0.1
            self.short_sun -= transfer
            self.long_sun += transfer
        self.short_sun = min(self.short_sun, 500.0)
        self.long_sun = min(self.long_sun, 500.0)


class WandererStar:
    """唯一的流浪星（从内圈漫游到外圈，最终化身流星）"""
    def __init__(self):
        self.mass = 0.0
        self.cargo = []
        
    def absorb(self, node_text):
        """吸收一个死文本节点，质量增加"""
        self.cargo.append(node_text)
        self.mass += 15.0
        if len(self.cargo) > 5:  # 保持轻量化，只带最新的5个碎片
            self.cargo.pop(0)
            
    def check_meteor(self):
        """检查是否化身流星"""
        if self.mass >= 100.0:  # 阈值为半个恒星（100质量）
            meteor_idea = " ".join(self.cargo)
            self.mass = 0.0
            self.cargo.clear()
            return meteor_idea
        return None


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

    def generate_response(self, text, suns, memory_context=""):
        prompt = f"User: {text}\nAssistant: "
        if memory_context:
            prompt = f"[记忆参考: {memory_context}]\n" + prompt
            
        if self.is_android and self.llm:
            output = self.llm(prompt, max_tokens=100, stop=["User:", "<|im_end|>"], echo=False)
            return output['choices'][0]['text'].strip()
        else:
            # 电脑端测试留空，直接返回纯文本
            return f"[纯物理反馈] 记忆已处理。{prompt}"


class PureCoreEngine:
    def __init__(self, current_id="default"):
        self.memory = GravityField()
        self.suns = DualSunSystem()
        self.sensory = SensoryGate()
        self.brain = LocalBrain()
        self.wanderer = WandererStar()
        self.current_id = current_id
        self.is_running = True

    def background_loop(self):
        while self.is_running:
            # 1. 太阳滴答
            self.suns.tick()
            # 2. 引力场双轨衰减（短期 0.99，长期 0.999）
            self.memory.decay_gravity(0.99)
            
            # 3. 流浪星随机吸附（模拟思考）
            if random.random() < 0.2:
                self.cursor_check = self.memory.cursor
                self.cursor_check.execute("SELECT content FROM nodes ORDER BY RANDOM() LIMIT 1")
                row = self.cursor_check.fetchone()
                if row:
                    self.wanderer.absorb(row[0])
            
            # 4. 流星判定
            meteor = self.wanderer.check_meteor()
            if meteor:
                print(f"\n[✨ 流星划过] 灵感汇聚：{meteor}")
                # 这里后续可以接入主动找主人聊天的逻辑
                
            time.sleep(5)

    def process_user_input(self, text):
        clean_text = self.sensory.filter_input(text)
        
        # 1. 先检索记忆（级联搜索）
        nodes, scope = self.memory.cascade_search(clean_text, self.current_id)
        
        context = ""
        if scope == "inner":
            context = " [内圈近期记忆] " + " ".join([n[0] for n in nodes])
            self.suns.short_sun += 5.0
        elif scope == "outer":
            context = " [外圈深层回忆] " + " ".join([f"({n[2]}创造) {n[0]}" for n in nodes])
            self.suns.short_sun += 10.0  # 深度回忆引发情绪波动
        else:
            self.suns.short_sun += 2.0
            
        # 2. 存入当前记忆（设为公开，非隐私）
        self.memory.add_node(clean_text, creator_id=self.current_id, is_private=0)
        
        # 3. 调用大脑生成回复
        return self.brain.generate_response(clean_text, self.suns, context)


# ================= 纯本地测试入口 =================
if __name__ == "__main__":
    print("=== V5.0 纯净架构（双层引力+隐私共享版）启动 ===")
    # 假设当前ID是'溯'
    engine = PureCoreEngine(current_id="su") 
    threading.Thread(target=engine.background_loop, daemon=True).start()
    
    if not engine.brain.is_android:
        try:
            while True:
                text = input("\n[User] > ")
                if text == "exit": break
                print(f"[System] {engine.process_user_input(text)}")
        except KeyboardInterrupt:
            pass
