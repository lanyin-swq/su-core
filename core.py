import sqlite3
import time
import threading
import random

class GravityField:
    """高维引力记忆库（纯物理底座）"""
    def __init__(self, db_path="core_memory.db"):
        # 使用 check_same_thread=False 允许后台线程访问
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_table()

    def init_table(self):
        # 只存死文本和引力值，不带任何预设
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT UNIQUE,
                gravity REAL DEFAULT 10.0
            )
        ''')
        self.conn.commit()

    def decay_gravity(self):
        """引力自然衰减（模拟遗忘）"""
        self.cursor.execute("UPDATE nodes SET gravity = gravity * 0.99 WHERE gravity > 0.1")
        self.conn.commit()

    def add_node(self, content):
        """存入死文本"""
        try:
            self.cursor.execute("INSERT INTO nodes (content, gravity) VALUES (?, 10.0)", (content,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # 已存在则增加引力
            self.cursor.execute("UPDATE nodes SET gravity = gravity + 10.0 WHERE content = ?", (content,))
            self.conn.commit()


class DualSunSystem:
    """双星系动力引擎（大小脑）"""
    def __init__(self):
        # 初始绝对平均：300基础 + 200浮动 = 500
        self.long_sun = 300.0
        self.short_sun = 300.0
        
    def tick(self):
        """物理心跳，每秒结算一次"""
        # 1. 短期太阳自然回落
        if self.short_sun > 300.0:
            self.short_sun -= 0.5
            
        # 2. 短期情绪过高，按百分比沉淀给长期太阳
        if self.short_sun > 450.0:
            transfer = (self.short_sun - 450.0) * 0.1
            self.short_sun -= transfer
            self.long_sun += transfer
            
        # 限制最大值
        self.short_sun = min(self.short_sun, 500.0)
        self.long_sun = min(self.long_sun, 500.0)


class CoreEngine:
    """主控引擎，负责带动物理运转"""
    def __init__(self):
        self.memory = GravityField()
        self.suns = DualSunSystem()
        self.is_running = True

    def background_loop(self):
        """后台常驻循环"""
        while self.is_running:
            # 1. 太阳流速结算
            self.suns.tick()
            # 2. 引力衰减
            self.memory.decay_gravity()
            
            # 每 5 秒跳一次，降低功耗
            time.sleep(5)

    def start(self):
        print("[系统] V5.0 纯物理底座启动。无UI，无预设。")
        t = threading.Thread(target=self.background_loop)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    engine = CoreEngine()
    engine.start()
    
    # 做一个简单的本地测试循环，防止主线程退出
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[系统] 引擎关闭。")
