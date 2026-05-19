# 人均消费数据展示面板

一个精美的数据展示网页，展示各国人均GDP、人口及各类食品人均消费量数据。

## 功能特性

### 🗺️ 地图展示
- 世界地图展示，不同颜色表示不同数值
- 鼠标悬浮显示国家名称和各项数据
- 点击国家高亮并显示详细信息

### 📊 数据表格
- 支持所有列排序（包括肉类细分项）
- 支持国家模糊查询
- 支持国家筛选（复选框）
- 显示中文国家/地区名称
- 计算并显示GDP总量列

### 🔍 筛选功能
- 左侧复选框筛选国家
- 搜索框支持模糊查询（按中文名或英文名）
- 全选/全不选/反选按钮
- "只显示被选中的"按钮

### 📱 响应式设计
- 适配不同屏幕尺寸
- 移动端友好

## 数据说明

### 数据来源
- **GDP**: Bolt and van Zanden – Maddison Project Database 2023
- **人口**: United Nations – World Population Prospects (2024)
- **食品消费**: Food and Agriculture Organization of the United Nations (2025)

### 数据单位
- **GDP**: 国际元（2011年价格），基于购买力平价（PPP）
- **消费数据**: kg/人/年

### 数据时效
- GDP数据: 2022年
- 其他数据: 2023年

## 技术栈

- **前端**: HTML5 + CSS3 + JavaScript (ES6+)
- **库**: jQuery 3.x + DataTables.js + ECharts
- **数据处理**: Python (uv)
- **部署**: 纯静态文件

## 项目结构

```
showpercapita/
├── data/                          # 原始数据文件
│   ├── fruit-consumption-per-capita/
│   ├── gdp-per-capita-maddison-project-database/
│   ├── per-capita-egg-consumption-kilograms-per-year/
│   ├── per-capita-meat-type/
│   ├── per-capita-milk-consumption/
│   ├── population-with-un-projections/
│   └── vegetable-consumption-per-capita/
├── web/                           # 前端文件
│   ├── index.html                 # 主页面
│   ├── css/
│   │   └── style.css              # 自定义样式
│   ├── js/
│   │   └── app.js                 # 主要JavaScript逻辑
│   ├── data/
│   │   └── processed-data.json    # 处理后的数据
│   └── lib/                       # 第三方库
│       ├── jquery.min.js
│       ├── datatables.min.js
│       ├── datatables.min.css
│       ├── echarts.min.js
│       └── world.json
├── tests/                         # 测试文件
│   └── test_process_data.py
├── process_data.py                # 数据处理脚本
├── requirements.txt               # Python依赖
├── country_mapping.json           # 中英文国家名称映射
└── README.md                      # 项目说明
```

## 快速开始

### 1. 数据处理

```bash
# 安装依赖
uv pip install -r requirements.txt

# 运行数据处理脚本
uv run process_data.py
```

### 2. 启动本地服务器

```bash
# 进入web目录
cd web

# 启动Python简单HTTP服务器
python3 -m http.server 8000

# 或者使用Node.js
npx serve .
```

### 3. 访问页面

在浏览器中打开: http://localhost:8000

## 使用说明

### 地图展示
1. 点击"🗺️ 地图展示"标签页
2. 鼠标悬浮查看国家数据
3. 点击国家查看详细信息并跳转到表格

### 数据表格
1. 点击"📊 数据表格"标签页
2. 使用左侧筛选面板选择国家
3. 点击表头进行排序
4. 使用搜索框进行模糊查询

### 筛选功能
- **全选**: 选中所有国家
- **全不选**: 取消所有选择
- **反选**: 反转当前选择
- **只显示被选中的**: 仅显示选中的国家

## 数据格式

处理后的数据格式 (`web/data/processed-data.json`):

```json
{
  "metadata": {
    "generated_at": "2026-05-19T11:53:28.386758",
    "gdp_year": 2022,
    "other_year": 2023,
    "total_countries": 259,
    "note": "GDP数据基于购买力平价（PPP），单位为国际元（2011年价格）"
  },
  "countries": [
    {
      "code": "CHN",
      "nameEn": "China",
      "nameZh": "中国",
      "population": 1422584930,
      "gdpPerCapita": 19238.18,
      "gdpTotal": 27367944948627.402,
      "meat": {
        "total": 115.2199994,
        "pig": 42.16,
        "beef": 7.8899994,
        "sheep": 4.02,
        "poultry": 18.71,
        "other": 0.76,
        "fish": 41.68
      },
      "milk": 34.77,
      "egg": 22.96,
      "vegetable": 412.71997,
      "fruit": 114.35999
    }
  ]
}
```

## 测试

```bash
# 运行测试
uv run pytest tests/test_process_data.py -v
```

## 部署

### 静态文件部署
项目是纯静态文件，可以部署到任何静态文件服务器：

- **GitHub Pages**: 直接推送web目录
- **Netlify**: 连接GitHub仓库，设置发布目录为web
- **Vercel**: 连接GitHub仓库，框架预设选择Other
- **Cloudflare Pages**: 连接GitHub仓库

### 本地部署
```bash
# 使用Python
cd web && python3 -m http.server 8000

# 使用Node.js
cd web && npx serve .

# 使用PHP
cd web && php -S localhost:8000
```

## 注意事项

1. **数据缺失**: 部分国家某些年份数据可能缺失，显示为"—"
2. **单位统一**: 所有消费数据单位为 kg/人/年
3. **货币单位**: GDP数据使用国际元（2011年价格）
4. **数据时效**: 最新数据为2023年（GDP为2022年）

## 许可证

本项目数据来自 Our World in Data，遵循其数据使用条款。

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### 2026-05-19
- 初始版本发布
- 支持地图展示和数据表格
- 支持国家筛选和排序功能
- 添加响应式设计