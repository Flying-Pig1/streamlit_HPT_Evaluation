import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = 'result_hpto1.1_hpto1.2_cogvlm2.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(file_path)

# 提取评分数据
ratings_data = {
    "hpto1.1": df["hpto1.1_rating"],
    "hpto1.2": df["hpto1.2_rating"],
    "cogvlm2": df["cogvlm2_rating"]
}

# 将字典转换为DataFrame以便于绘图
ratings_df = pd.DataFrame(ratings_data)

# 定义柱子的宽度
bar_width = 0.2

# 定义每个评分位置
ratings = np.arange(1, 6)

# 计算每个模型的柱子位置
hpto1_1_positions = ratings - bar_width
hpto1_2_positions = ratings
cogvlm2_positions = ratings + bar_width

# 计算每个模型的平均分
hpto1_1_mean = ratings_df["hpto1.1"].mean()
hpto1_2_mean = ratings_df["hpto1.2"].mean()
cogvlm2_mean = ratings_df["cogvlm2"].mean()

# 绘制直方图
plt.figure(figsize=(12, 8))

# 为每个评分绘制直方图
plt.bar(hpto1_1_positions, ratings_df["hpto1.1"].value_counts().reindex(ratings, fill_value=0),
        width=bar_width, label=f'hpto1.1 (mean={hpto1_1_mean:.2f})')
plt.bar(hpto1_2_positions, ratings_df["hpto1.2"].value_counts().reindex(ratings, fill_value=0),
        width=bar_width, label=f'hpto1.2 (mean={hpto1_2_mean:.2f})')
plt.bar(cogvlm2_positions, ratings_df["cogvlm2"].value_counts().reindex(ratings, fill_value=0),
        width=bar_width, label=f'cogvlm2 (mean={cogvlm2_mean:.2f})')

plt.xlabel('Ratings')
plt.ylabel('Frequency')
plt.title('Distribution of Ratings')
plt.xticks(ratings)
plt.legend(loc='upper right')

plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig('distribution_of_ratings.png')
plt.show()
