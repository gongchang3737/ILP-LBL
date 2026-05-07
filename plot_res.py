# # -*- coding: utf-8 -*-
# """
# 绘制 12 个散点图 + 一个共用色条，基于给定实验结果表格。
# 横轴：求解质量（single 用 precision %，multiple 用 F1 %）；
# 纵轴：求解时间（秒）；
# 每张图只包含同一 Scenario × 数据集 × 问题类型；
# 颜色对应不同方法（ME、ME-LBL、LP、LP-LBL、ILP、ILP-LBL），所有图共用一个色条。
# """

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

# # 设置中文字体 & 负号显示
# # plt.rcParams['font.sans-serif'] = ['SimHei']
# # plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['axes.unicode_minus'] = False

# # 方法名称与颜色映射
# methods = ["ME", "ME-LBL", "LP", "LP-LBL", "ILP", "ILP-LBL"]
# method_to_idx = {m:i for i,m in enumerate(methods)}
# method_to_color = {
#     "ME":      "#FEB7B0",
#     "ME-LBL":  "#F9220A",
#     "LP":      "#9AD7FF",
#     "LP-LBL":  "#0485FD",
#     "ILP":     "#9AFEC4",
#     "ILP-LBL": "#03A747",
# }

# # --- 构造数据 ---
# rows = []
# def add_block(dataset, scenario, single_precisions, single_times, mult_f1s, mult_times):
#     for m, p, t in zip(methods, single_precisions, single_times):
#         rows.append({
#             "dataset": dataset,
#             "scenario": scenario,
#             "problem": "single",
#             "method": m,
#             "method_idx": method_to_idx[m],
#             "quality": p,    # precision (%)
#             "time": t
#         })
#     for m, f, t in zip(methods, mult_f1s, mult_times):
#         rows.append({
#             "dataset": dataset,
#             "scenario": scenario,
#             "problem": "multiple",
#             "method": m,
#             "method_idx": method_to_idx[m],
#             "quality": f,    # F1-score (%)
#             "time": t
#         })

# # G2：Noise-free
# add_block(
#     "G2","Noise-free",
#     single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
#     single_times=[0.3594,0.3681,0.5292,0.6469,0.7480,0.8838],
#     mult_f1s=[82.13,67.05,82.13,67.05,82.13,67.05],
#     mult_times=[0.2506,0.3109,0.3602,0.3882,1.0652,0.5879]
# )
# # G2：Probabilistic Propagation
# add_block(
#     "G2","Probabilistic Propagation",
#     single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
#     single_times=[0.3426,0.4222,0.5173,0.7197,0.7314,0.8302],
#     mult_f1s=[95.77,71.39,95.77,71.39,95.77,71.39],
#     mult_times=[0.2585,0.2796,0.3601,0.4200,0.6399,0.4333]
# )
# # G2：Observation Error
# add_block(
#     "G2","Observation Error",
#     single_precisions=[50.26,13.47,51.81,12.95,67.88,32.54],
#     single_times=[0.4180,0.4608,0.5464,0.8670,2.4400,0.6459],
#     mult_f1s=[34.27,26.30,49.45,20.67,63.00,31.14],
#     mult_times=[0.2564,0.2046,0.3638,0.4013,2.1175,0.4629]
# )
# # G3：Noise-free
# add_block(
#     "G3","Noise-free",
#     single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
#     single_times=[13.6602,11.0153,20.0177,16.9239,73.4500,30.9897],
#     mult_f1s=[90.85,90.29,90.85,90.29,90.85,90.29],
#     mult_times=[1.2463,0.8923,2.9568,1.0669,8.5357,5.1239]
# )
# # G3：Probabilistic Propagation
# add_block(
#     "G3","Probabilistic Propagation",
#     single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
#     single_times=[15.5577,16.7458,13.8099,16.9787,26.8886,29.1060],
#     mult_f1s=[99.32,98.30,99.32,98.30,99.32,98.30],
#     mult_times=[1.0783,1.0869,1.1735,1.2674,2.1723,1.2975]
# )
# # G3：Observation Error
# add_block(
#     "G3","Observation Error",
#     single_precisions=[27.80,2.32,34.70,10.72,54.43,42.14],
#     single_times=[16.4999,14.4339,19.0498,19.6285,412.5471,112.7180],
#     mult_f1s=[24.55,19.81,26.60,18.00,43.63,32.06],
#     mult_times=[1.6068,1.0574,1.9394,1.2751,32.9666,3.2436]
# )

# df = pd.DataFrame(rows)
# print(df)

# # --- 绘图参数 ---
# output_dir = "./scatter_plots"
# os.makedirs(output_dir, exist_ok=True)

# norm = Normalize(vmin=-0.5, vmax=len(methods)-0.5)
# cmap = plt.get_cmap()  # 默认色图

# def draw_chart(sub_df, ax, title):
#     for m in methods:
#         d_m = sub_df[sub_df["method"] == m]
#         if d_m.empty:
#             continue
#         ax.scatter(
#             d_m["quality"],
#             d_m["time"],
#             color=method_to_color[m],
#             s=80,
#             alpha=0.9,
#             edgecolors="white",
#             linewidth=0.7,
#             label=None  # 各子图无需图例
#         )
#     ax.set_xlabel("solution quality (%)")
#     ax.set_ylabel("solution time (s)")
#     # ax.set_title(title)
#     ax.set_xlim(0, 105)
#     ax.set_yscale("log")
#     # ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.3)
#     ax.grid(True, axis='x', linestyle="--", linewidth=0.8, alpha=1.0)
#     ax.text(0.5, -0.22, title, transform=ax.transAxes,
#                     ha='center', va='top', fontsize=10)
    
# # --- 布局：3 行 × 4 列 共 12 子图 ---
# fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 12), dpi=150)
# axes_list = axes.flatten()

# idx = 0
# for scenario in ["Noise-free", "Probabilistic Propagation", "Observation Error"]:
#     for dataset in ["G2", "G3"]:
#         for problem in ["single", "multiple"]:
#             sub = df[(df["scenario"] == scenario) &
#                      (df["dataset"] == dataset) &
#                      (df["problem"] == problem)]
#             title = f"({idx+1}) {scenario} | {dataset} | {'Single' if problem=='single' else 'Multiple'}"
#             draw_chart(sub, axes_list[idx], title)
#             idx += 1

# # --- 统一图例（放在所有子图之上或之下）---
# # 在空白区域创建一个 legend
# handles = [plt.Line2D([0], [0], marker='o', color=method_to_color[m], linestyle='', 
#                       label=m, markersize=10, markeredgecolor='white') 
#            for m in methods]
# fig.legend(handles=handles, labels=methods, loc='upper center', 
#            ncol=len(methods), bbox_to_anchor=(0.5, 0.95), frameon=False)

# plt.tight_layout(rect=[0, 0, 1, 0.93])  # 留出顶部空间给 legend
# # plt.show()
# fig.savefig(os.path.join(output_dir, "exp_res.png"))
# plt.close(fig)

# print("绘图完成，整体图片保存在：", output_dir)


### 绘制TI、QI、EI散点图
plt.rcParams['axes.unicode_minus'] = False

# 方法名称与颜色映射
methods_base = ["ME", "LP", "ILP"]
methods = ["ME", "ME-LBL", "LP", "LP-LBL", "ILP", "ILP-LBL"]
method_to_idx = {m:i for i,m in enumerate(methods)}
print("method_to_idx:", method_to_idx)
colors_no_lbl = ["#b4fcbb", "#6ff86f", "#068728"]   # 色系 A
colors_lbl    = ["#fbbabb", "#ff8a8a", "#f70505"]   # 色系 B
method_to_color = {
    "ME":      colors_no_lbl[0],
    "LP":      colors_no_lbl[1],
    "ILP":     colors_no_lbl[2],
    "ME-LBL":  colors_lbl[0],
    "LP-LBL":  colors_lbl[1],
    "ILP-LBL": colors_lbl[2],
}
method_to_color = {
    "ME":      "#9AD7FF",
    "ME-LBL":  "#0485FD",
    "LP":      "#9AFEC4",
    "LP-LBL":  "#03A747",
    "ILP":     "#FEB7B0",
    "ILP-LBL": "#F9220A",
}

# --- 构造数据 ---
rows = []
def add_block(dataset, scenario, single_precisions, single_times, mult_f1s, mult_times):
    # 计算ME、LP、ILP的EI值
    for m in methods_base:
        single_time_improvement = (single_times[method_to_idx[m]+1] / single_times[method_to_idx[m]]) - 1
        single_quality_improvement = (single_precisions[method_to_idx[m]+1] / single_precisions[method_to_idx[m]]) - 1
        # EI = single_time_improvement / single_quality_improvement - 1
        # 使用np.where处理除零情况，避免ZeroDivisionError
        if single_quality_improvement == 0:  # 避免除零错误
            EI = np.sign(single_time_improvement) * np.inf
        else:
            EI = single_time_improvement / single_quality_improvement - 1
        rows.append({
            "dataset": dataset,
            "scenario": scenario,
            "problem": "single",
            "method_base": m,
            "method_idx": method_to_idx[m],
            "quality_improvement": single_quality_improvement,    # precision (%)
            "time_improvement": single_time_improvement,   # time (%)
            "EI": EI
        })
        multiple_quality_improvement = (mult_f1s[method_to_idx[m]+1] / mult_f1s[method_to_idx[m]]) - 1
        multiple_time_improvement = (mult_times[method_to_idx[m]+1] / mult_times[method_to_idx[m]]) - 1
        # 使用np.where处理除零情况，避免ZeroDivisionError
        if multiple_quality_improvement == 0:  # 避免除零错误
            EI = np.sign(multiple_time_improvement) * np.inf
        else:
            EI = multiple_time_improvement / multiple_quality_improvement - 1
        rows.append({
            "dataset": dataset,
            "scenario": scenario,
            "problem": "multiple",
            "method_base": m,
            "method_idx": method_to_idx[m],
            "quality_improvement": multiple_quality_improvement,    # precision (%)
            "time_improvement": multiple_time_improvement,   # time (%)
            "EI": EI
        })

# G2：Noise-free
add_block(
    "G2","Noise-free",
    single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
    single_times=[0.3594,0.3681,0.5292,0.6469,0.7480,0.8838],
    mult_f1s=[82.13,67.05,82.13,67.05,82.13,67.05],
    mult_times=[0.2506,0.3109,0.3602,0.3882,1.0652,0.5879]
)
# G2：Probabilistic Propagation
add_block(
    "G2","Probabilistic Propagation",
    single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
    single_times=[0.3426,0.4222,0.5173,0.7197,0.7314,0.8302],
    mult_f1s=[95.77,71.39,95.77,71.39,95.77,71.39],
    mult_times=[0.2585,0.2796,0.3601,0.4200,0.6399,0.4333]
)
# G2：Observation Error
add_block(
    "G2","Observation Error",
    single_precisions=[50.26,13.47,51.81,12.95,67.88,32.54],
    single_times=[0.4180,0.4608,0.5464,0.8670,2.4400,0.6459],
    mult_f1s=[34.27,26.30,49.45,20.67,63.00,31.14],
    mult_times=[0.2564,0.2046,0.3638,0.4013,2.1175,0.4629]
)
# G3：Noise-free
add_block(
    "G3","Noise-free",
    single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
    single_times=[13.6602,11.0153,20.0177,16.9239,73.4500,30.9897],
    mult_f1s=[90.85,90.29,90.85,90.29,90.85,90.29],
    mult_times=[1.2463,0.8923,2.9568,1.0669,8.5357,5.1239]
)
# G3：Probabilistic Propagation
add_block(
    "G3","Probabilistic Propagation",
    single_precisions=[100.00,100.00,100.00,100.00,100.00,100.00],
    single_times=[15.5577,16.7458,13.8099,16.9787,26.8886,29.1060],
    mult_f1s=[99.32,98.30,99.32,98.30,99.32,98.30],
    mult_times=[1.0783,1.0869,1.1735,1.2674,2.1723,1.2975]
)
# G3：Observation Error
add_block(
    "G3","Observation Error",
    single_precisions=[27.80,2.32,34.70,10.72,54.43,42.14],
    single_times=[16.4999,14.4339,19.0498,19.6285,412.5471,112.7180],
    mult_f1s=[24.55,19.81,26.60,18.00,43.63,32.06],
    mult_times=[1.6068,1.0574,1.9394,1.2751,32.9666,3.2436]
)

df = pd.DataFrame(rows)
print(df)

# 绘制含有两个子图的散点图。其中，第一个子图基于dataset=G2的数据，第二个子图基于dataset=G3的数据。
# 在每个子图中，scenario决定散点的形状，分别使用三角形、五角星、圆形；
# problem决定散点颜色深浅，single是浅色，multiple是深色；
# method_base决定散点的具体颜色，ME使用红色、LP使用蓝色、ILP使用绿色。
# 每个子图中，横轴使用quality_improvement和纵轴使用time_improvement
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs = axs.flatten()  # 展平为一维数组便于索引
method_problem_to_color = {
    "ME":{"single":"#FEB7B0", "multiple":"#F9220A"},    
    "LP":{"single":"#9AD7FF", "multiple":"#0485FD"},
    "ILP":{"single":"#9AFEC4", "multiple":"#03A747"},
}

for i, ax in enumerate(axs):
    dataset = "G2" if i == 0 else "G3"
    df_dataset = df[df["dataset"] == dataset]
    for scenario, marker in zip(["Noise-free", "Probabilistic Propagation", "Observation Error"], ["^", "*", "o"]):
        df_scenario = df_dataset[df_dataset["scenario"] == scenario]
        for problem in ["single", "multiple"]:
            for method_base in methods_base:
                df_problem = df_scenario[df_scenario["problem"] == problem]
                df_method = df_problem[df_problem["method_base"] == method_base]
                color = method_problem_to_color[method_base][problem]
                x = df_method["quality_improvement"]
                y = df_method["time_improvement"]
                # 将坐标(x, y)中的较大值限定在[-1,1]范围内，另外较小值等比例缩小
                if np.max(np.abs(x)) > 1 or np.max(np.abs(y)) > 1:
                    ratio = np.maximum(np.abs(x), np.abs(y)) / 1.0
                    x = x / ratio
                    y = y / ratio
                # x = np.clip(x, -1, 1)
                # y = np.clip(y, -1, 1)
                label = ""
                if problem == "single":
                    label += "Sin-"
                elif problem == "multiple":
                    label += "Multi-"

                if scenario == "Noise-free":
                    label += "NF-"
                elif scenario == "Probabilistic Propagation":
                    label += "PP-"
                elif scenario == "Observation Error":
                    label += "OE-"
                
                if method_base == "ME":
                    label += "ME"
                elif method_base == "LP":
                    label += "LP"
                elif method_base == "ILP":
                    label += "ILP"

                # 调整散点大小，默认为20
                ax.scatter(x, y, color=color, marker=marker, label=label, s=80) 
                ax.set_xlabel("Quality Difference (%)")
                ax.set_ylabel("Time Difference (%)")
                if dataset == "G2":
                    ax.set_title("(a) $G_2$")
                else:
                    ax.set_title("(b) $G_3$")
                # ax.set_title("%s" % dataset)
                # ax.legend(methods_base)
                ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.3)
                ax.set_xlim(-1.05, 1.05)
                ax.set_ylim(-1.05, 1.05)
                ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.7)
                ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.7)

    # ax.legend(["single", "multiple"])
    # ax.legend(["Noise-free", "Probabilistic Propagation", "Observation Error"])
    # ax.legend(methods_base)
    # ax.legend(["single", "multiple"])
    # ax.legend(["Noise-free", "Probabilistic Propagation", "Observation Error"])
    # 加上y=x线
    ax.plot([-2, 2], [-2, 2], color='gray', linestyle='--')
# 在两个子图右侧统一放置图例
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1)) # 默认将含有label的图形对象放到图例中 
# plt.legend(loc)

plt.tight_layout()
# plt.savefig('scatter_plots/exp_res_eff.png')
plt.show()