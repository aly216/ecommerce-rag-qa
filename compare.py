"""
无 RAG vs 有 RAG 对照实验

用途：同一个问题，分别走「裸问 DeepSeek」和「RAG 检索增强」两条路径回答，
直观对比检索增强带来的差异（无 RAG 只有通用常识，有 RAG 答案有据可依）。

运行：python compare.py
"""
import config_data as config
from rag import RAGService

# 想对比的问题，改这里即可
QUESTIONS = [
    "我身高172体重140斤穿什么码",
    "羊毛大衣怎么洗",
    "黄皮肤适合什么颜色",
]

# 复用同一个 RAG 实例
rag = RAGService()


def no_rag(question: str) -> str:
    """A 路径：直接问 DeepSeek，不带检索上下文"""
    return config.model.invoke(question).content


def with_rag(question: str) -> str:
    """B 路径：走 RAG 链（检索 → 拼上下文 → 生成）"""
    return rag.chain.invoke({"input": question}, config.session_config)


if __name__ == "__main__":
    for q in QUESTIONS:
        print("=" * 70)
        print(f"问题：{q}")
        print("=" * 70)

        print("\n【无 RAG】直接问 DeepSeek：")
        print("-" * 70)
        print(no_rag(q))

        print("\n【有 RAG】检索 + 生成：")
        print("-" * 70)
        print(with_rag(q))
        print()
