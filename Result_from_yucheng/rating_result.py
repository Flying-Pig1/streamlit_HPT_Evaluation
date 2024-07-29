import pandas as pd
import matplotlib.pyplot as plt


def process_csv(file_path, output_file_path):
    # 读取CSV文件，尝试不同编码
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    # 提取需要的列并添加 id 和 task 列
    df_extracted = df[["image_name", "question", "difficulty", "question_type", "hpto1_1_rating", "cogvlm2_rating",
                       "glm4v_rating"]].copy()

    # 添加 id 列
    df_extracted["id"] = range(1, len(df_extracted) + 1)

    # 提取 task 并添加到新列
    df_extracted["task"] = df_extracted["image_name"].apply(
        lambda x: x.split('_')[1].lower() if len(x.split('_')) > 1 else "")

    # 规范difficulty大小写
    df_extracted["difficulty"] = df_extracted["difficulty"].apply(lambda x: x.lower())

    # 重新排列列顺序
    columns_order = ["id", "image_name", "question", "task", "difficulty", "question_type", "hpto1_1_rating",
                     "cogvlm2_rating", "glm4v_rating"]
    df_extracted = df_extracted[columns_order]

    # 保存修改后的CSV文件
    df_extracted.to_csv(output_file_path, index=False, encoding='utf-8')

    print(f'Modified CSV file saved to {output_file_path}')

    return df_extracted


def plot_task(df):
    tasks = df['task'].unique()
    models = ['hpto1_1_rating', 'glm4v_rating', 'cogvlm2_rating']

    avg_scores = []
    for task in tasks:
        task_df = df[df['task'] == task]
        avg_scores.append({
            'task': task,
            'hpto1_1': task_df['hpto1_1_rating'].mean(),
            'glm4v': task_df['glm4v_rating'].mean(),
            'cogvlm2': task_df['cogvlm2_rating'].mean(),
            #'average': task_df[models].mean(axis=1).mean()
        })

    avg_scores_df = pd.DataFrame(avg_scores)
    avg_scores_df.set_index('task', inplace=True)

    avg_scores_df.plot(kind='bar', figsize=(12, 8))
    plt.title('Average Scores by Task for Each Model')
    plt.ylabel('Average Score')
    plt.xlabel('Task')
    plt.legend(title='Model')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('statistic_task.png')
    plt.show()

def plot_difficulty(df):
    difficulties = df['difficulty'].unique()
    models = ['hpto1_1_rating', 'glm4v_rating', 'cogvlm2_rating']

    avg_scores = []
    for difficulty in difficulties:
        difficulty_df = df[df['difficulty'] == difficulty]
        avg_scores.append({
            'difficulty': difficulty,
            'hpto1_1': difficulty_df['hpto1_1_rating'].mean(),
            'glm4v': difficulty_df['glm4v_rating'].mean(),
            'cogvlm2': difficulty_df['cogvlm2_rating'].mean(),
            #'average': difficulty_df[models].mean(axis=1).mean()
        })

    avg_scores_df = pd.DataFrame(avg_scores)
    avg_scores_df.set_index('difficulty', inplace=True)
    avg_scores_df = avg_scores_df.reindex(['easy', 'medium', 'difficult'])

    avg_scores_df.plot(kind='bar', figsize=(12, 8))
    plt.title('Average Scores by Difficulty for Each Model')
    plt.ylabel('Average Score')
    plt.xlabel('Difficulty')
    plt.legend(title='Model')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('statistic_difficulty.png')
    plt.show()

file_path = 'result.csv'  # 替换为你的输入文件路径
output_file_path = 'rating_result.csv'  # 替换为你想要保存的文件路径
process_csv(file_path, output_file_path)
df_extracted = process_csv(file_path, output_file_path)
# 画出每个模型每个任务上的平均分，以及三个模型在该任务的平均分
plot_task(df_extracted)
plot_difficulty(df_extracted)