import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 数据
brands = ['BYD', 'Proton', 'Tesla', 'Zeekr', 'Chery']
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

sales = {
    'BYD': [2159, 2500, 3351, 6397],
    'Proton': [1738, 2000, 2216, 2936],
    'Tesla': [627, 1200, 1339, 4116],
    'Zeekr': [200, 300, 600, 1460],
    'Chery': [150, 250, 400, 745]
}

# 颜色
colors = {
    'BYD': '#1E88E5',      # 蓝色
    'Proton': '#43A047',   # 绿色
    'Tesla': '#E53935',    # 红色
    'Zeekr': '#FB8C00',    # 橙色
    'Chery': '#8E24AA'     # 紫色
}

# 创建图表
fig, ax = plt.subplots(figsize=(12, 7))

for brand in brands:
    ax.plot(quarters, sales[brand], marker='o', linewidth=2.5, markersize=8, 
            label=brand, color=colors[brand])
    # 添加数据标签
    for i, (q, v) in enumerate(zip(quarters, sales[brand])):
        ax.annotate(f'{v:,}', (q, v), textcoords="offset points", 
                   xytext=(0, 10), ha='center', fontsize=9, color=colors[brand])

ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
ax.set_ylabel('Units Sold', fontsize=12, fontweight='bold')
ax.set_title('2025 Malaysia EV Sales by Brand (Quarterly)', fontsize=16, fontweight='bold', pad=20)

ax.legend(loc='upper left', fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_ylim(0, 7500)

# 添加总计说明
total_2025 = 44813
ax.text(0.98, 0.02, f'Total EV Sales 2025: {total_2025:,} units\n(+105.7% YoY)', 
        transform=ax.transAxes, fontsize=10, ha='right', va='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('/Users/caidengyong/.openclaw/workspace/temp/ev_sales_chart.png', dpi=150, bbox_inches='tight')
print("图表已保存")
