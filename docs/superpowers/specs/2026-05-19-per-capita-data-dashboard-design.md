# 人均消费数据展示面板设计文档

## 项目概述

创建一个精美的数据展示网页，展示各国人均GDP、人口及各类食品人均消费量数据。使用jQuery + DataTables.js + ECharts技术栈，提供良好的用户体验和交互功能。

### 目标
- 展示2023年数据（GDP使用2022年数据）
- 支持所有列排序（包括肉类细分项）
- 支持国家模糊查询
- 支持国家筛选（复选框）
- 显示中文国家/地区名称
- 计算并显示GDP总量列
- 纯静态部署，无需服务器

## 数据处理流程

### 数据源
1. **人均GDP**: `gdp-per-capita-maddison-project-database.csv` (2022年)
2. **人口**: `population-with-un-projections.csv` (2023年)
3. **肉类和水产消费**: `per-capita-meat-type.csv` (2023年)
   - 猪肉 (Pork)
   - 牛肉 (Beef and buffalo)
   - 羊肉 (Sheep and goat)
   - 禽肉 (Poultry)
   - 其他肉类 (Other meats)
   - 水产 (Fish and seafood)
4. **奶类**: `per-capita-milk-consumption.csv` (2023年)
5. **蛋类**: `per-capita-egg-consumption-kilograms-per-year.csv` (2023年)
6. **蔬菜**: `vegetable-consumption-per-capita.csv` (2023年)
7. **水果**: `fruit-consumption-per-capita.csv` (2023年)

### 处理步骤
1. 使用uv运行Python脚本读取所有CSV文件
2. 筛选2023年数据（GDP用2022年）
3. 计算GDP总量 = 人均GDP × 人口
4. 创建中英文国家名称映射表
5. 合并所有数据为JSON格式
6. 输出到 `web/data/processed-data.json`

### 数据格式
```json
{
  "countries": [
    {
      "code": "CHN",
      "nameEn": "China",
      "nameZh": "中国",
      "population": 1425893465,
      "gdpPerCapita": 12556,
      "gdpTotal": 17911252039540,
      "meat": {
        "total": 62.1,
        "pig": 34.7,
        "beef": 8.3,
        "sheep": 4.2,
        "poultry": 14.9,
        "other": 0.0,
        "fish": 45.2
      },
      "milk": 45.2,
      "egg": 23.1,
      "vegetable": 350.2,
      "fruit": 130.5
    }
  ]
}
```

## 页面布局设计

### 整体布局
- **顶部**: 标题和描述
- **标签页**: 地图展示 / 数据表格（两个独立标签页）
- **左侧**: 筛选面板（宽度25%）
- **右侧**: 数据表格（宽度75%）
- **底部**: 分页和统计信息

### 标签页设计
1. **地图展示标签页**：
   - 世界地图展示
   - 鼠标悬浮显示数据
   - 点击国家显示详情
2. **数据表格标签页**：
   - 左侧筛选面板
   - 右侧数据表格
   - 底部分页和统计

### 筛选面板
1. **搜索框**: 支持模糊查询（按中文名或英文名）
2. **操作按钮**:
   - 全选
   - 全不选
   - 反选
   - 只显示被选中的
3. **国家列表**: 复选框列表，按字母顺序显示中文名

### 数据表格列（带emoji）
1. 🌍 国家/地区（中文名）
2. 👥 人口
3. 💰 人均GDP (国际元)
4. 💎 GDP总量 (国际元)
5. 🥩 肉类消费总量 (kg/人/年)
6. 🐷 猪肉 (kg/人/年)
7. 🐂 牛肉 (kg/人/年)
8. 🐑 羊肉 (kg/人/年)
9. 🐔 禽肉 (kg/人/年)
10. 🦌 其他肉类 (kg/人/年)
11. 🐟 水产 (kg/人/年)
12. 🥛 奶类 (kg/人/年)
13. 🥚 蛋类 (kg/人/年)
14. 🥬 蔬菜 (kg/人/年)
15. 🍎 水果 (kg/人/年)

## 功能设计

### 地图展示功能
- 世界地图展示，不同颜色表示不同数值
- 鼠标悬浮显示国家名称和各项数据
- 点击国家高亮并显示详细信息
- 地图与表格数据联动

### 排序功能
- 点击表头切换升序/降序
- 默认按GDP总量降序排列
- 支持所有列排序

### 筛选功能
- 左侧复选框筛选国家
- 搜索框支持模糊查询（按中文名或英文名）
- 全选/全不选/反选按钮
- "只显示被选中的"按钮

### 数据展示
- 数字格式化（千分位分隔符）
- 科学计数法转换为可读格式
- 缺失数据显示为"—"

### 响应式设计
- 适配不同屏幕尺寸
- 移动端友好

## 技术实现

### 文件结构
```
web/
├── index.html          # 主页面
├── css/
│   └── style.css       # 自定义样式
├── js/
│   └── app.js          # 主要JavaScript逻辑
├── data/
│   └── processed-data.json  # 处理后的数据
└── lib/
    ├── jquery.min.js   # jQuery 3.x
    ├── datatables.min.js # DataTables核心
    ├── datatables.min.css # DataTables样式
    ├── echarts.min.js  # ECharts
    └── world.json      # 世界地图GeoJSON数据
```

### 第三方库
1. **jQuery 3.x**: DOM操作和事件处理
2. **DataTables.js**: 表格功能（排序、分页、搜索）
3. **ECharts**: 数据可视化，包括地图展示

### 技术栈
- 前端: HTML5 + CSS3 + JavaScript (ES6+)
- 库: jQuery + DataTables.js + ECharts
- 数据处理: uv (Python包管理器)
- 部署: 纯静态文件

## 部署说明

### 本地运行
1. 使用uv处理数据: `uv run process_data.py`
2. 在浏览器中打开 `web/index.html`

### 生产部署
- 纯静态文件，可部署到任何静态文件服务器
- 支持GitHub Pages、Netlify、Vercel等平台
- 无需服务器端处理

## 数据来源

所有数据来自 Our World in Data，原始数据来自以下来源：
- GDP: Bolt and van Zanden – Maddison Project Database 2023
- 人口: United Nations – World Population Prospects (2024)
- 食品消费: Food and Agriculture Organization of the United Nations (2025)

## 注意事项

1. **数据缺失**: 部分国家某些年份数据可能缺失，显示为"—"
2. **单位统一**: 所有消费数据单位为 kg/人/年
3. **货币单位**: GDP数据使用国际元（2011年价格）
4. **数据时效**: 最新数据为2023年（GDP为2022年）

## 后续扩展

1. 添加数据可视化图表（ECharts）
2. 支持数据导出（CSV、Excel）
3. 添加历史趋势对比
4. 支持多语言切换
