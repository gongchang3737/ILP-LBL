# 单源、无噪音
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np  #当前为numpy=2.0.2,numexpr=2.10.2, pandas=2.3.2
import copy
import pandas as pd
from guro_opt import *
import time
import json
# import networkx.utils

# 绘制结果图
LBL = ['SL', 'MLSL']
problem = ['single', 'multiple']
methods = ['ME', 'LP', 'ILP']
noise = ['PP','OE']  # OE: 观测误差; PP: 概率传播

quality_data = pd.DataFrame()
time_data = pd.DataFrame()


quality_data['error_prop_list'] = list(np.arange(0.00, 0.51, 0.01))
time_data['error_prop_list'] = list(np.arange(0.00, 0.51, 0.01))
quality_data['prop_prob_list'] = list(np.arange(0.50, 1.01, 0.01))
time_data['prop_prob_list'] = list(np.arange(0.50, 1.01, 0.01))

for l in LBL:
    for p in problem:
        for n in noise:
            for m in methods:
                filename = 'results/'+l+'_'+p+'_'+m+'_'+n+'_L3.json'
                print(filename)
                with open('results/'+l+'_'+p+'_'+m+'_'+n+'_L3.json', 'r') as f:
                    results = json.load(f)
                quality_data[l+'_'+p+'_'+m+'_'+n] = results['precision']
                time_data[l+'_'+p+'_'+m+'_'+n] = results['time']

print(quality_data)
print(time_data)
# 搜索其中有没有nan、inf、-inf和0
# print((quality_data == 0).values.any())

# print((time_data == 0).values.any())

# 绘制一张4个子图的图像，存为.png格式
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()  # 展平为一维数组便于索引
i = 0

lines = []
labels = []

### 绘制效率图
for p in problem:
    for n in noise:
        if n == 'OE':
            x = quality_data['error_prop_list']
            y_scale = [0, 31]
        else:
            x = quality_data['prop_prob_list']
            y_scale = [20, 51]
        ax = axes[i]
        i += 1

        # 设定颜色为浅红、浅蓝、浅绿
        ax.set_prop_cycle('color', ['#FCB2AF', '#9BDFDF', '#D2E9CB'])
        for m in methods:
            # for l in LBL:
            
            # 对于每一行，计算SL_time和MLSL_time的差值除以SL_time，得到求解时间降低百分比
            time_improvement = (time_data['MLSL'+'_'+p+'_'+m+'_'+n] / time_data['SL'+'_'+p+'_'+m+'_'+n]) - 1
            # 对于每一行，计算SL_quality和MLSL_quality的差值除以SL_quality，得到求解质量降低百分比
            quality_improvement = (quality_data['MLSL'+'_'+p+'_'+m+'_'+n] / quality_data['SL'+'_'+p+'_'+m+'_'+n]) - 1
            # print(quality_improvement)
            print((quality_improvement[y_scale[0]:y_scale[1]] == 0).values.any())
            if (quality_improvement[y_scale[0]:y_scale[1]] == 0).values.any():
                print(p+'_'+m+'_'+n)
                # print(quality_improvement)
            
            # 计算Eff. Improv. = -np.sign(time_improvement) * np.abs(time_improvement) / np.abs(quality_improvement) - 1
            y = -time_improvement / np.abs(quality_improvement) - 1
            for ind in range(len(y)):
                if quality_improvement[ind] == 0:
                    y[ind] = -np.inf * np.sign(time_improvement[ind])  # 如果quality_improvement为0，根据time_improvement设定符号
            # print(y)
            x_plot = x[y_scale[0]:y_scale[1]]
            y_plot = y[y_scale[0]:y_scale[1]]
            
            y_plot = y_plot.replace([np.inf, -np.inf], [5, -5]) # 将其中的inf值替换为+1，-inf值替换为-1
            # 将高于100和低于-100的节点值替换为1和-1
            y_plot = y_plot.apply(lambda v: 5 if v > 5 else (-5 if v < -5 else v))
            # plt.figure(figsize=(7, 5))
            # 按照set_prop_cycle设定的颜色顺序绘制曲线
            line, = ax.plot(x_plot, y_plot, marker="o", zorder=1, label=m)
            # 设定 X 轴范围和刻度
            ax.set_ylim(-6, 6)
            ax.set_yticks(np.arange(-5, 6, 1)) # 生成 -5 到 5，步长为 1 的数组
            if i == 1:  # 只在第一次循环时保存图例标签
                lines.append(line)
                labels.append(m)
            # 筛选出y_plot中的1和-1的索引
            good_indices = np.where(y_plot == 5)[0].tolist()
            if n == 'PP':
                good_indices = [i+20 for i in good_indices]
            x_good = x_plot[good_indices]
            y_good = y_plot[good_indices]
            bad_indices =  np.where(y_plot == -5)[0].tolist()
            if n == 'PP':
                bad_indices = [i+20 for i in bad_indices]
            x_bad = x_plot[bad_indices]
            y_bad = y_plot[bad_indices]
            
            # good点使用绿色圆点，bad点使用红色圆点标记为散点
            ax.scatter(x_good, y_good, c='g', marker="*", zorder=2, s=10)
            ax.scatter(x_bad, y_bad, c='r', marker="*", zorder=3, s=10)
            # 加上曲线Y=0，使用灰色，线条较细
            ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.7, label='y=0')
            if n == 'OE':
                ax.set_xlabel("$P_e$")
            else:
                ax.set_xlabel("$P_r$")
            ax.set_ylabel("Eff. improv.")
            # 生成 (a), (b), (c), (d) 标签
            label = chr(ord('a') + i-1) 
            ax.set_title(f"({label}) {p} & {n}")
            # ax.set_title(p+' & '+n)
            # ax.set_title(p+'_'+m+'_'+n)
            # plt.grid(True)
            # ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.3)

# 添加统一图例
# fig.legend(lines, labels, loc='upper right', bbox_to_anchor=(0.9, 0.9))
# 添加统一图例到顶部
fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), 
           ncol=len(labels), frameon=False)
# 调整布局以给顶部图例留出空间
plt.subplots_adjust(top=0.9)
plt.show()
# plt.savefig('scatter_plots/sensitivity.png')
# plt.show()

# # 写入xlsx文件
# quality_data.to_excel('results/quality_data.xlsx', index=False)
# time_data.to_excel('results/time_data.xlsx', index=False)

# ### 绘制求解质量-时间（1/x）散点图
# import pandas as pd
# import matplotlib.pyplot as plt

# # 1. 读入数据（第一行是表头）
# df = pd.read_excel("results/test_res.xlsx")

# # 2. 绘制散点图：横轴时间，纵轴质量
# plt.figure(figsize=(7, 5))

# # 将求解时间取1/x，便于展示
# df["SL_time"] = 1 / df["SL_time"]
# df["MLSL_time"] = 1 / df["MLSL_time"]

# plt.scatter(df["SL_time"][0:30], df["SL_quality"][0:30],
#             label="SL", marker="o", alpha=0.7)

# plt.scatter(df["MLSL_time"][0:30], df["MLSL_quality"][0:30],
#             label="MLSL", marker="s", alpha=0.7)

# plt.xlabel("Solution time (s)")
# plt.ylabel("Solution quality")
# plt.title("Solution quality vs. time")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # 绘制效率提升百分比图像
# # 对于每一行，计算SL_time和MLSL_time的差值除以SL_time，得到求解时间降低百分比
# df["time_improvement"] = (df["SL_time"] - df["MLSL_time"]) / df["SL_time"] * 100
# # 对于每一行，计算SL_quality和MLSL_quality的差值除以SL_quality，得到求解质量降低百分比
# df["quality_improvement"] = (df["SL_quality"] - df["MLSL_quality"]) / df["SL_quality"] * 100
# # 计算商
# df["improvement_ratio"] = df["time_improvement"] / df["quality_improvement"]
# # 绘制error_prop_list与improvement_ratio的关系图
# plt.figure(figsize=(7, 5))
# plt.plot(df["error_prop_list"][0:30], df["improvement_ratio"][0:30], marker="o")
# # 加上曲线Y=1，使用红色
# plt.axhline(y=1, color='r', linestyle='--', label='y=1')
# plt.xlabel("Error Propagation Rate")
# plt.ylabel("Improvement Ratio")
# plt.title("Error Propagation Rate vs. Improvement Ratio")
# plt.grid(True)
# plt.tight_layout()
# plt.show()
