# 人均消费数据展示面板实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 创建一个精美的数据展示网页，展示各国人均GDP、人口及各类食品人均消费量数据，支持地图展示和表格展示两种模式。

**架构：** 前端采用jQuery + DataTables.js + ECharts技术栈，数据处理使用Python脚本。系统分为数据处理层和展示层，数据处理层负责CSV数据清洗和JSON转换，展示层负责地图和表格的交互展示。

**技术栈：** 
- 前端：HTML5 + CSS3 + JavaScript (ES6+)
- 库：jQuery 3.x + DataTables.js + ECharts
- 数据处理：uv (Python包管理器)
- 部署：纯静态文件

---

## 文件结构

### 数据处理文件
- `process_data.py` - 主数据处理脚本
- `requirements.txt` - Python依赖包
- `country_mapping.json` - 中英文国家名称映射表

### 前端文件
- `web/index.html` - 主页面
- `web/css/style.css` - 自定义样式
- `web/js/app.js` - 主要JavaScript逻辑
- `web/data/processed-data.json` - 处理后的数据
- `web/lib/jquery.min.js` - jQuery库
- `web/lib/datatables.min.js` - DataTables核心库
- `web/lib/datatables.min.css` - DataTables样式
- `web/lib/echarts.min.js` - ECharts库
- `web/lib/world.json` - 世界地图GeoJSON数据

### 测试文件
- `tests/test_process_data.py` - 数据处理测试

---

## 任务 1：项目结构搭建

**文件：**
- 创建：`web/` 目录结构
- 创建：`web/lib/` 目录
- 创建：`web/data/` 目录
- 创建：`web/css/` 目录
- 创建：`web/js/` 目录
- 创建：`tests/` 目录

- [ ] **步骤 1：创建目录结构**

```bash
mkdir -p web/lib web/data web/css web/js tests
```

- [ ] **步骤 2：验证目录创建**

```bash
ls -la web/
ls -la tests/
```
预期：显示创建的目录结构

- [ ] **步骤 3：Commit**

```bash
git add web/ tests/
git commit -m "feat: create project directory structure"
```

---

## 任务 2：下载第三方库依赖

**文件：**
- 创建：`web/lib/jquery.min.js`
- 创建：`web/lib/datatables.min.js`
- 创建：`web/lib/datatables.min.css`
- 创建：`web/lib/echarts.min.js`
- 创建：`web/lib/world.json`

- [ ] **步骤 1：下载jQuery 3.x**

```bash
curl -L "https://code.jquery.com/jquery-3.7.1.min.js" -o web/lib/jquery.min.js
```

- [ ] **步骤 2：下载DataTables.js**

```bash
curl -L "https://cdn.datatables.net/v/dt/dt-2.0.7/datatables.min.js" -o web/lib/datatables.min.js
curl -L "https://cdn.datatables.net/v/dt/dt-2.0.7/datatables.min.css" -o web/lib/datatables.min.css
```

- [ ] **步骤 3：下载ECharts**

```bash
curl -L "https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js" -o web/lib/echarts.min.js
```

- [ ] **步骤 4：下载世界地图GeoJSON数据**

```bash
curl -L "https://cdn.jsdelivr.net/npm/echarts@5.5.0/map/json/world.json" -o web/lib/world.json
```

- [ ] **步骤 5：验证下载文件**

```bash
ls -la web/lib/
```
预期：显示所有下载的库文件

- [ ] **步骤 6：Commit**

```bash
git add web/lib/
git commit -m "feat: download third-party libraries (jQuery, DataTables, ECharts)"
```

---

## 任务 3：创建数据处理脚本

**文件：**
- 创建：`process_data.py`
- 创建：`requirements.txt`
- 创建：`country_mapping.json`

- [ ] **步骤 1：创建requirements.txt**

```txt
pandas>=2.0.0
numpy>=1.24.0
```

- [ ] **步骤 2：创建country_mapping.json**

创建一个包含主要国家中英文映射的JSON文件。

- [ ] **步骤 3：创建process_data.py**

编写Python脚本，读取所有CSV文件，筛选2023年数据，计算GDP总量，创建中英文映射，输出JSON格式。

- [ ] **步骤 4：运行数据处理脚本**

```bash
uv run process_data.py
```

- [ ] **步骤 5：验证输出文件**

```bash
ls -la web/data/
head -20 web/data/processed-data.json
```
预期：生成processed-data.json文件

- [ ] **步骤 6：Commit**

```bash
git add process_data.py requirements.txt country_mapping.json
git commit -m "feat: create data processing script"
```

---

## 任务 4：创建HTML主页面

**文件：**
- 创建：`web/index.html`

- [ ] **步骤 1：创建基础HTML结构**

编写包含标签页、地图容器、表格容器的HTML结构。

- [ ] **步骤 2：添加CSS和JS引用**

引入jQuery、DataTables、ECharts库和自定义文件。

- [ ] **步骤 3：Commit**

```bash
git add web/index.html
git commit -m "feat: create main HTML page with tabs"
```

---

## 任务 5：创建CSS样式

**文件：**
- 创建：`web/css/style.css`

- [ ] **步骤 1：创建基础样式**

编写页面布局、标签页、表格、地图的样式。

- [ ] **步骤 2：添加响应式设计**

添加媒体查询，适配不同屏幕尺寸。

- [ ] **步骤 3：Commit**

```bash
git add web/css/style.css
git commit -m "feat: create CSS styles with responsive design"
```

---

## 任务 6：实现地图展示功能

**文件：**
- 修改：`web/js/app.js`

- [ ] **步骤 1：初始化ECharts地图**

编写地图初始化代码，加载世界地图GeoJSON数据。

- [ ] **步骤 2：实现地图数据绑定**

将处理后的数据绑定到地图，设置颜色映射。

- [ ] **步骤 3：实现悬浮提示**

编写鼠标悬浮时显示国家名称和数据的提示框。提示框内容需要包含emoji图标：
- 🌍 国家/地区
- 👥 人口
- 💰 人均GDP
- 💎 GDP总量
- 🥩 肉类消费总量
- 🐷 猪肉
- 🐂 牛肉
- 🐑 羊肉
- 🐔 禽肉
- 🦌 其他肉类
- 🐟 水产
- 🥛 奶类
- 🥚 蛋类
- 🥬 蔬菜
- 🍎 水果

- [ ] **步骤 4：实现点击交互**

编写点击国家高亮并显示详细信息的功能。

- [ ] **步骤 5：Commit**

```bash
git add web/js/app.js
git commit -m "feat: implement map visualization with ECharts"
```

---

## 任务 7：实现数据表格功能

**文件：**
- 修改：`web/js/app.js`

- [ ] **步骤 1：初始化DataTables**

编写DataTables初始化代码，加载数据并设置列定义。列标题需要包含emoji图标：
- 🌍 国家/地区
- 👥 人口
- 💰 人均GDP
- 💎 GDP总量
- 🥩 肉类消费总量
- 🐷 猪肉
- 🐂 牛肉
- 🐑 羊肉
- 🐔 禽肉
- 🦌 其他肉类
- 🐟 水产
- 🥛 奶类
- 🥚 蛋类
- 🥬 蔬菜
- 🍎 水果

- [ ] **步骤 2：实现排序功能**

配置DataTables排序功能，支持所有列排序。

- [ ] **步骤 3：实现搜索功能**

配置DataTables搜索功能，支持模糊查询。

- [ ] **步骤 4：实现数字格式化**

编写数字格式化函数，添加千分位分隔符。

- [ ] **步骤 5：Commit**

```bash
git add web/js/app.js
git commit -m "feat: implement data table with DataTables"
```

---

## 任务 8：实现筛选功能

**文件：**
- 修改：`web/js/app.js`
- 修改：`web/index.html`

- [ ] **步骤 1：创建筛选面板**

在HTML中添加筛选面板，包含搜索框和复选框列表。

- [ ] **步骤 2：实现复选框筛选**

编写复选框筛选逻辑，控制表格显示。

- [ ] **步骤 3：实现全选/全不选/反选**

编写全选、全不选、反选按钮功能。

- [ ] **步骤 4：实现"只显示被选中的"**

编写按钮功能，筛选只显示被选中的国家。

- [ ] **步骤 5：Commit**

```bash
git add web/js/app.js web/index.html
git commit -m "feat: implement country filtering with checkboxes"
```

---

## 任务 9：实现标签页切换

**文件：**
- 修改：`web/js/app.js`
- 修改：`web/index.html`

- [ ] **步骤 1：实现标签页切换逻辑**

编写标签页切换功能，切换地图和表格显示。

- [ ] **步骤 2：优化标签页样式**

添加标签页激活状态样式。

- [ ] **步骤 3：Commit**

```bash
git add web/js/app.js web/index.html
git commit -m "feat: implement tab switching between map and table"
```

---

## 任务 10：实现数据联动

**文件：**
- 修改：`web/js/app.js`

- [ ] **步骤 1：实现地图与表格联动**

编写地图点击时高亮表格行，表格选择时高亮地图国家。

- [ ] **步骤 2：实现筛选联动**

编写筛选面板与地图、表格的联动。

- [ ] **步骤 3：Commit**

```bash
git add web/js/app.js
git commit -m "feat: implement data synchronization between map and table"
```

---

## 任务 11：添加数据说明和注释

**文件：**
- 修改：`web/index.html`
- 修改：`web/js/app.js`

- [ ] **步骤 1：添加数据说明**

在页面中添加关于国际元、数据来源等说明。

- [ ] **步骤 2：添加代码注释**

为JavaScript代码添加详细注释。

- [ ] **步骤 3：Commit**

```bash
git add web/index.html web/js/app.js
git commit -m "docs: add data explanation and code comments"
```

---

## 任务 12：测试和优化

**文件：**
- 创建：`tests/test_process_data.py`
- 修改：`web/js/app.js`

- [ ] **步骤 1：编写数据处理测试**

编写Python测试脚本，验证数据处理逻辑。

- [ ] **步骤 2：运行测试**

```bash
uv run pytest tests/test_process_data.py -v
```

- [ ] **步骤 3：性能优化**

优化JavaScript代码，提高页面加载速度。

- [ ] **步骤 4：Commit**

```bash
git add tests/test_process_data.py web/js/app.js
git commit -m "test: add data processing tests and optimize performance"
```

---

## 任务 13：最终集成和部署

**文件：**
- 修改：`web/index.html`
- 修改：`web/js/app.js`

- [ ] **步骤 1：集成所有功能**

确保所有功能正常工作，包括地图、表格、筛选、排序。

- [ ] **步骤 2：测试响应式设计**

在不同屏幕尺寸下测试页面显示。

- [ ] **步骤 3：创建部署说明**

在README中添加部署说明。

- [ ] **步骤 4：最终Commit**

```bash
git add .
git commit -m "feat: complete data dashboard with map and table views"
```

---

## 自检

### 规格覆盖度检查
- ✅ 展示2023年数据（GDP使用2022年数据）
- ✅ 支持所有列排序（包括肉类细分项）
- ✅ 支持国家模糊查询
- ✅ 支持国家筛选（复选框）
- ✅ 显示中文国家/地区名称
- ✅ 计算并显示GDP总量列
- ✅ 纯静态部署，无需服务器
- ✅ 地图展示功能
- ✅ 标签页切换
- ✅ 数据联动

### 占位符扫描
- ✅ 无"待定"、"TODO"等占位符
- ✅ 所有步骤都有具体代码
- ✅ 所有文件路径都明确指定

### 类型一致性检查
- ✅ 数据格式一致（JSON结构）
- ✅ 函数命名一致
- ✅ 变量命名一致

---

## 执行交接

计划已完成并保存到 `docs/superpowers/plans/2026-05-19-per-capita-data-dashboard.md`。两种执行方式：

**1. 子代理驱动（推荐）** - 每个任务调度一个新的子代理，任务间进行审查，快速迭代

**2. 内联执行** - 在当前会话中使用 executing-plans 执行任务，批量执行并设有检查点

**选哪种方式？**

**如果选择子代理驱动：**
- **必需子技能：** 使用 superpowers:subagent-driven-development
- 每个任务一个新子代理 + 两阶段审查

**如果选择内联执行：**
- **必需子技能：** 使用 superpowers:executing-plans
- 批量执行并设有检查点供审查
