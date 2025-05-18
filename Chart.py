import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df3 = pd.read_csv('Danhgia3.csv')
df4 = pd.read_csv('Danhgia4.csv')

df3['Puzzle Size'] = '3x3'
df4['Puzzle Size'] = '4x4'

df_combined = pd.concat([df3, df4])

heuristics = df3['Heuristic'].unique()

colors = plt.cm.tab10.colors

# 1. Biểu đồ cột về thời gian trung bình
plt.figure(figsize=(12, 6))
bar_width = 0.15
index = np.arange(2)

for i, heuristic in enumerate(heuristics):
    data = df_combined[df_combined['Heuristic'] == heuristic]
    plt.bar(index + i * bar_width,
            data['Avg Time (successful)'],
            width=bar_width,
            label=heuristic,
            color=colors[i])

plt.xlabel('Kích thước Puzzle')
plt.ylabel('Thời gian trung bình (giây)')
plt.title('So sánh thời gian thực thi trung bình của các heuristic')
plt.xticks(index + bar_width * (len(heuristics) - 1) / 2, ['3x3 Puzzle', '4x4 Puzzle'])
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 2. Biểu đồ cột về số bước giải trung bình
plt.figure(figsize=(12, 6))
for i, heuristic in enumerate(heuristics):
    data = df_combined[df_combined['Heuristic'] == heuristic]
    plt.bar(index + i * bar_width,
            data['Avg Solution Length'],
            width=bar_width,
            label=heuristic,
            color=colors[i])

plt.xlabel('Kích thước Puzzle')
plt.ylabel('Số bước giải trung bình')
plt.title('So sánh độ dài lời giải trung bình của các heuristic')
plt.xticks(index + bar_width * (len(heuristics) - 1) / 2, ['3x3 Puzzle', '4x4 Puzzle'])
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 3. Biểu đồ cột về số trạng thái được duyệt
plt.figure(figsize=(12, 6))
for i, heuristic in enumerate(heuristics):
    data = df_combined[df_combined['Heuristic'] == heuristic]
    plt.bar(index + i * bar_width,
            data['Avg Visited States'],
            width=bar_width,
            label=heuristic,
            color=colors[i])

plt.xlabel('Kích thước Puzzle')
plt.ylabel('Số trạng thái được duyệt trung bình')
plt.title('So sánh số trạng thái được duyệt của các heuristic')
plt.xticks(index + bar_width * (len(heuristics) - 1) / 2, ['3x3 Puzzle', '4x4 Puzzle'])
plt.legend()
plt.yscale('log')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

metrics = ['Avg Time (successful)', 'Avg Solution Length', 'Avg Visited States']
metric_names = ['Thời gian (giây)', 'Số bước giải', 'Số trạng thái']
scaling_factors = {}

plt.figure(figsize=(15, 5))
for j, (metric, name) in enumerate(zip(metrics, metric_names)):
    plt.subplot(1, 3, j + 1)
    for i, heuristic in enumerate(heuristics):
        data = df_combined[df_combined['Heuristic'] == heuristic]
        values = data[metric].values
        plt.plot(['3x3', '4x4'], values, marker='o', label=heuristic, color=colors[i])

        if metric == 'Avg Time (successful)':
            scaling_factors[heuristic] = values[1] / values[0]

    plt.xlabel('Kích thước puzzle')
    plt.ylabel(name)
    plt.title(f'Ảnh hưởng của kích thước puzzle\nđến {name.lower()}')
    if j == 2:
        plt.yscale('log')
    plt.grid(True)
    if j == 0:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()