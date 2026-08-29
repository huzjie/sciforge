# -*- coding: utf-8 -*-
"""启动控制面示例（FastAPI 优先，stdlib 兜底）。"""
from sciforge.cli import main

if __name__ == "__main__":
    main(["serve", "--host", "0.0.0.0", "--port", "8000"])
