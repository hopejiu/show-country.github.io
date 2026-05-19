/**
 * 人均消费数据展示面板 - 主应用脚本
 * 包含地图展示、数据表格、筛选功能、状态持久化等
 */

// 全局变量
let mapChart = null;
let dataTable = null;
let allData = [];
let selectedCountries = new Set();

// localStorage key前缀
const STORAGE_PREFIX = 'showpercapita_';

// ========== 状态持久化工具 ==========

function saveState(key, value) {
    try {
        localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value));
    } catch (e) {
        console.warn('状态保存失败:', key, e);
    }
}

function loadState(key, defaultValue) {
    try {
        const raw = localStorage.getItem(STORAGE_PREFIX + key);
        return raw ? JSON.parse(raw) : defaultValue;
    } catch (e) {
        return defaultValue;
    }
}

// ========== 初始化 ==========

$(document).ready(function() {
    console.log('应用初始化开始...');
    loadData();
    initTabs();
    initFilters();
    console.log('应用初始化完成');
});

// ========== 数据加载 ==========

function loadData() {
    $.getJSON('assets/processed-data.json', function(data) {
        allData = data.countries;
        console.log('数据加载成功:', allData.length, '个国家');
        initMap();
        initDataTable();
        initCountryList();
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error('数据加载失败:', textStatus, errorThrown);
        alert('数据加载失败，请检查网络连接或刷新页面重试。');
    });
}

// ========== 标签页切换（带持久化） ==========

function initTabs() {
    // 恢复上次的标签页
    const savedTab = loadState('activeTab', 'table');
    $('.tab-button[data-tab="' + savedTab + '"]').click();

    $('.tab-button').click(function() {
        const tabId = $(this).data('tab');
        $('.tab-button').removeClass('active');
        $(this).addClass('active');
        $('.tab-content').removeClass('active');
        $('#' + tabId + '-tab').addClass('active');

        // 持久化标签页
        saveState('activeTab', tabId);

        // 切换到地图时调整大小
        if (tabId === 'map' && mapChart) {
            setTimeout(function() { mapChart.resize(); }, 100);
        }
    });
}

// ========== 地图 ==========

// 指标名称映射（字段路径 → 中文名）
var INDICATOR_META = {
    gdpPerCapita: { name: '💰 人均GDP', unit: '国际元', max: 80000 },
    gdpTotal: { name: '💎 GDP总量', unit: '国际元', max: 30000000000000 },
    population: { name: '👥 人口', unit: '人', max: 1500000000 },
    'meat.total': { name: '🥩 肉类总量', unit: 'kg/人/年', max: 150 },
    'meat.pig': { name: '🐷 猪肉', unit: 'kg/人/年', max: 70 },
    'meat.beef': { name: '🐂 牛肉', unit: 'kg/人/年', max: 50 },
    'meat.sheep': { name: '🐑 羊肉', unit: 'kg/人/年', max: 30 },
    'meat.poultry': { name: '🐔 禽肉', unit: 'kg/人/年', max: 60 },
    'meat.other': { name: '🦌 其他肉类', unit: 'kg/人/年', max: 10 },
    'meat.fish': { name: '🐟 水产', unit: 'kg/人/年', max: 90 },
    milk: { name: '🥛 奶类', unit: 'kg/人/年', max: 300 },
    egg: { name: '🥚 蛋类', unit: 'kg/人/年', max: 25 },
    vegetable: { name: '🥬 蔬菜', unit: 'kg/人/年', max: 400 },
    fruit: { name: '🍎 水果', unit: 'kg/人/年', max: 200 },
    lifeExpectancy: { name: '⏳ 预期寿命', unit: '岁', max: 85 },
    energy: { name: '⚡ 人均能源', unit: 'kWh/人/年', max: 200000 }
};

// 指标字段路径解析（支持嵌套如 'meat.total'）
function getMapValue(country, indicator) {
    var parts = indicator.split('.');
    var val = country;
    for (var i = 0; i < parts.length; i++) {
        val = val[parts[i]];
        if (val == null) return 0;
    }
    return val;
}

// 当前地图指标，持久化
var currentMapIndicator = loadState('mapIndicator', 'gdpPerCapita');

function calcPercentile(values, p) {
    if (!values.length) return null;
    var sorted = values.slice().sort(function(a, b) { return a - b; });
    var idx = Math.floor(sorted.length * p / 100);
    return sorted[Math.min(idx, sorted.length - 1)] || 1;
}

function updateMap() {
    if (!mapChart) return;
    if (!INDICATOR_META[currentMapIndicator]) { currentMapIndicator = 'gdpPerCapita'; }
    var meta = INDICATOR_META[currentMapIndicator];
    var data = allData
        .filter(function(c) { return c.code !== 'OWID_WRL'; })
        .map(function(c) {
            var val = getMapValue(c, currentMapIndicator);
            // null/undefined 视为 0
            return { name: c.nameEn, value: (val == null ? 0 : val), countryData: c };
        });
    // 10~90分位数，忽略0值
    var values = data.map(function(d) { return d.value; }).filter(function(v) { return v > 0; });
    var minVal = calcPercentile(values, 10) || 0;
    var maxVal = calcPercentile(values, 90) || meta.max;
    var vMin = Math.floor(minVal), vMax = Math.ceil(maxVal);
    if (vMin >= vMax) { vMin = 0; vMax = Math.ceil(Math.max.apply(null, values)) || meta.max; }
    mapChart.setOption({
        title: { text: meta.name + ' 分布地图' },
        visualMap: { min: vMin, max: vMax },
        series: [{ data: data }]
    });
}

function initMap() {
    $.getJSON('assets/world.json', function(worldJson) {
        echarts.registerMap('world', worldJson);
        mapChart = echarts.init(document.getElementById('map-chart'));

        // 兼容旧版 localStorage 中的旧指标 key（如 meatTotal → meat.total）
        if (!INDICATOR_META[currentMapIndicator]) { currentMapIndicator = 'gdpPerCapita'; }
        var meta = INDICATOR_META[currentMapIndicator];
        var data = allData
            .filter(function(c) { return c.code !== 'OWID_WRL'; })
            .map(function(c) {
                var val = getMapValue(c, currentMapIndicator);
                return { name: c.nameEn, value: (val == null ? 0 : val), countryData: c };
            });
        var values = data.map(function(d) { return d.value; }).filter(function(v) { return v > 0; });
        var minVal = calcPercentile(values, 10) || 0;
        var maxVal = calcPercentile(values, 90) || meta.max;
        var vMin = Math.floor(minVal), vMax = Math.ceil(maxVal);
        if (vMin >= vMax) { vMin = 0; vMax = Math.ceil(Math.max.apply(null, values)) || meta.max; }

        mapChart.setOption({
            title: {
                text: meta.name + ' 分布地图',
                subtext: '点击国家查看详细数据',
                left: 'center',
                textStyle: { fontSize: 18, fontWeight: 'bold' }
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) { return formatMapTooltip(params); }
            },
            visualMap: {
                min: vMin, max: vMax,
                text: ['高', '低'],
                realtime: false, calculable: true,
                inRange: { color: ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695'] },
                left: 'left', top: 'bottom'
            },
            series: [{
                name: meta.name, type: 'map', map: 'world', roam: true,
                emphasis: { label: { show: true, fontSize: 12, fontWeight: 'bold' }, itemStyle: { areaColor: '#ffd700' } },
                itemStyle: { borderColor: '#fff', borderWidth: 0.5 },
                data: data
            }]
        });

        mapChart.on('click', function(params) {
            if (params.data) { showCountryDetails(params.data); }
        });

        $(window).resize(function() {
            if (mapChart) { mapChart.resize(); }
        });

        // 绑定指标切换
        $('#map-indicator').val(currentMapIndicator);
        $('#map-indicator').change(function() {
            currentMapIndicator = $(this).val();
            saveState('mapIndicator', currentMapIndicator);
            updateMap();
        });

        console.log('地图初始化完成');
    }).fail(function() {
        console.error('世界地图数据加载失败');
        $('#map-chart').html('<div class="loading">地图数据加载失败</div>');
    });
}

function formatMapTooltip(params) {
    if (!params.data || !params.data.countryData) return params.name;
    var c = params.data.countryData;
    return '<div style="min-width:200px;">' +
        '<strong style="font-size:14px;">🌍 ' + c.nameZh + ' (' + c.nameEn + ')</strong><br>' +
        '<hr style="margin:5px 0;border-color:#ddd;">' +
        '<div style="display:grid;grid-template-columns:auto 1fr;gap:3px 10px;">' +
        '<span>👥 人口:</span><span>' + formatNumber(c.population) + '</span>' +
        '<span>💰 人均GDP:</span><span>' + formatGDP(c.gdpPerCapita) + ' 国际元</span>' +
        '<span>💎 GDP总量:</span><span>' + formatGDP(c.gdpTotal) + ' 国际元</span>' +
        '<span>🥩 肉类总量:</span><span>' + formatNumber(c.meat.total) + ' kg</span>' +
        '<span>🐷 猪肉:</span><span>' + formatNumber(c.meat.pig) + ' kg</span>' +
        '<span>🐂 牛肉:</span><span>' + formatNumber(c.meat.beef) + ' kg</span>' +
        '<span>🐑 羊肉:</span><span>' + formatNumber(c.meat.sheep) + ' kg</span>' +
        '<span>🐔 禽肉:</span><span>' + formatNumber(c.meat.poultry) + ' kg</span>' +
        '<span>🦌 其他肉类:</span><span>' + formatNumber(c.meat.other) + ' kg</span>' +
        '<span>🐟 水产:</span><span>' + formatNumber(c.meat.fish) + ' kg</span>' +
        '<span>🥛 奶类:</span><span>' + formatNumber(c.milk) + ' kg</span>' +
        '<span>🥚 蛋类:</span><span>' + formatNumber(c.egg) + ' kg</span>' +
        '<span>🥬 蔬菜:</span><span>' + formatNumber(c.vegetable) + ' kg</span>' +
        '<span>🍎 水果:</span><span>' + formatNumber(c.fruit) + ' kg</span>' +
        '<span>⏳ 预期寿命:</span><span>' + formatNumber(c.lifeExpectancy) + ' 岁</span>' +
        '<span>⚡ 人均能源:</span><span>' + formatNumber(c.energy) + ' kWh</span>' +
        '</div></div>';
}

function showCountryDetails(countryData) {
    // 点击地图国家时不再跳转到表格
    console.log('点击国家:', countryData.nameZh);
}

// ========== 数据表格（带持久化） ==========

function initDataTable() {
    var tableData = prepareTableData();

    dataTable = $('#data-table').DataTable({
        data: tableData,
        columns: [
            { title: '🌍 国家/地区', data: 'name' },
            { title: '👥 人口', data: 'population', className: 'number-cell' },
            { title: '💰 人均GDP', data: 'gdpPerCapita', className: 'number-cell' },
            { title: '💎 GDP总量', data: 'gdpTotal', className: 'number-cell' },
            { title: '🥩 肉类总量', data: 'meatTotal', className: 'number-cell' },
            { title: '🐷 猪肉', data: 'meatPig', className: 'number-cell' },
            { title: '🐂 牛肉', data: 'meatBeef', className: 'number-cell' },
            { title: '🐑 羊肉', data: 'meatSheep', className: 'number-cell' },
            { title: '🐔 禽肉', data: 'meatPoultry', className: 'number-cell' },
            { title: '🦌 其他肉类', data: 'meatOther', className: 'number-cell' },
            { title: '🐟 水产', data: 'meatFish', className: 'number-cell' },
            { title: '🥛 奶类', data: 'milk', className: 'number-cell' },
            { title: '🥚 蛋类', data: 'egg', className: 'number-cell' },
            { title: '🥬 蔬菜', data: 'vegetable', className: 'number-cell' },
            { title: '🍎 水果', data: 'fruit', className: 'number-cell' },
            { title: '⏳ 预期寿命', data: 'lifeExpectancy', className: 'number-cell' },
            { title: '⚡ 人均能源', data: 'energy', className: 'number-cell' }
        ],
        order: [[3, 'desc']],
        pageLength: 25,
        lengthMenu: [10, 25, 50, 100],
        language: {
            search: '🔍 搜索:',
            lengthMenu: '每页显示 _MENU_ 条',
            info: '显示 _START_ 到 _END_ 共 _TOTAL_ 条',
            infoEmpty: '没有数据',
            infoFiltered: '(从 _MAX_ 条中筛选)',
            paginate: { first: '首页', last: '末页', next: '下一页', previous: '上一页' }
        },
        dom: '<"top"fl>rt<"bottom"ip><"clear">',
        colReorder: true,
        stateSave: true,
        stateDuration: 0,  // 永不自动过期
        stateSaveCallback: function(settings, data) {
            try {
                localStorage.setItem(STORAGE_PREFIX + 'DataTables_data', JSON.stringify(data));
            } catch(e) { console.warn('表格状态保存失败:', e); }
        },
        stateLoadCallback: function(settings) {
            try {
                var saved = localStorage.getItem(STORAGE_PREFIX + 'DataTables_data');
                return saved ? JSON.parse(saved) : null;
            } catch(e) { return null; }
        },
        createdRow: function(row, data, dataIndex) {
            $(row).click(function() {
                $(this).toggleClass('selected');
                var code = data.code;
                if ($(this).hasClass('selected')) selectedCountries.add(code);
                else selectedCountries.delete(code);
                updateCheckboxState(code, $(this).hasClass('selected'));
                saveSelectedCountries();
            });
        }
    });

    // 绑定排序/搜索/分页变化时也保存筛选状态
    dataTable.on('order.dt search.dt page.dt length.dt', function() {
        saveSelectedCountries();
    });

    console.log('数据表格初始化完成');
}

function prepareTableData() {
    return allData
        .filter(function(c) { return c.code !== 'OWID_WRL'; })
        .map(function(c) {
            return {
                code: c.code,
                name: c.nameZh + ' (' + c.nameEn + ')',
                population: formatNumber(c.population),
                gdpPerCapita: formatGDP(c.gdpPerCapita),
                gdpTotal: formatGDP(c.gdpTotal),
                meatTotal: formatNumber(c.meat.total),
                meatPig: formatNumber(c.meat.pig),
                meatBeef: formatNumber(c.meat.beef),
                meatSheep: formatNumber(c.meat.sheep),
                meatPoultry: formatNumber(c.meat.poultry),
                meatOther: formatNumber(c.meat.other),
                meatFish: formatNumber(c.meat.fish),
                milk: formatNumber(c.milk),
                egg: formatNumber(c.egg),
                vegetable: formatNumber(c.vegetable),
                fruit: formatNumber(c.fruit),
                lifeExpectancy: formatNumber(c.lifeExpectancy),
                energy: formatNumber(c.energy)
            };
        });
}

// ========== 国家筛选列表（带持久化） ==========

function saveSelectedCountries() {
    saveState('selectedCountries', Array.from(selectedCountries));
}

function loadSelectedCountries() {
    var saved = loadState('selectedCountries', null);
    if (saved && saved.length > 0) {
        selectedCountries = new Set(saved);
    } else {
        // 默认全部选中
        allData.forEach(function(c) { selectedCountries.add(c.code); });
    }
}

function initCountryList() {
    var countryList = $('#country-list');
    countryList.empty();

    // 恢复选中国家
    loadSelectedCountries();

    var sortedCountries = allData
        .filter(function(c) { return c.code !== 'OWID_WRL'; })
        .sort(function(a, b) { return a.nameZh.localeCompare(b.nameZh, 'zh'); });

    sortedCountries.forEach(function(country) {
        var item = $('<div class="country-item"></div>');
        var isChecked = selectedCountries.has(country.code);
        var checkbox = $('<input type="checkbox" id="country-' + country.code + '" ' + (isChecked ? 'checked' : '') + '>');
        var label = $('<label for="country-' + country.code + '">' + country.nameZh + '</label>');

        item.append(checkbox).append(label);
        countryList.append(item);

        checkbox.change(function() {
            if ($(this).is(':checked')) selectedCountries.add(country.code);
            else selectedCountries.delete(country.code);
            filterTable();
            saveSelectedCountries();
        });
    });

    // 应用初始筛选
    filterTable();
    console.log('国家筛选列表初始化完成:', sortedCountries.length, '个国家');
}

// ========== 筛选按钮（带持久化） ==========

function initFilters() {
    // 恢复筛选面板可见性
    var filterVisible = loadState('filterVisible', true);
    if (!filterVisible) {
        $('#filter-panel').addClass('hidden');
        $('#show-filter').show();
    }

    // 搜索框
    $('#country-search').on('input', function() {
        var txt = $(this).val().toLowerCase();
        $('#country-list .country-item').each(function() {
            var name = $(this).find('label').text().toLowerCase();
            $(this).toggle(name.indexOf(txt) >= 0);
        });
    });

    // 全选
    $('#select-all').click(function() {
        $('#country-list input[type="checkbox"]').prop('checked', true);
        allData.forEach(function(c) { selectedCountries.add(c.code); });
        filterTable();
        saveSelectedCountries();
    });

    // 全不选
    $('#deselect-all').click(function() {
        $('#country-list input[type="checkbox"]').prop('checked', false);
        selectedCountries.clear();
        filterTable();
        saveSelectedCountries();
    });

    // 反选
    $('#invert-selection').click(function() {
        $('#country-list input[type="checkbox"]').each(function() {
            $(this).prop('checked', !$(this).is(':checked'));
            var code = $(this).attr('id').replace('country-', '');
            if ($(this).is(':checked')) selectedCountries.add(code);
            else selectedCountries.delete(code);
        });
        filterTable();
        saveSelectedCountries();
    });

    // 只显示被选中的
    $('#show-selected').click(function() {
        filterTable();
    });

    // 隐藏筛选面板
    $('#toggle-filter').click(function() {
        $('#filter-panel').addClass('hidden');
        $('#show-filter').show();
        saveState('filterVisible', false);
        if (dataTable) dataTable.columns.adjust().draw();
    });

    // 显示筛选面板
    $('#show-filter').click(function() {
        $('#filter-panel').removeClass('hidden');
        $(this).hide();
        saveState('filterVisible', true);
        if (dataTable) {
            setTimeout(function() { dataTable.columns.adjust().draw(); }, 300);
        }
    });

    // 导出CSV
    $('#export-csv').click(function() {
        exportCSV();
    });

    console.log('筛选功能初始化完成');
}

// ========== 辅助函数 ==========

function updateCheckboxState(countryCode, isChecked) {
    var cb = $('#country-' + countryCode);
    if (cb.length) cb.prop('checked', isChecked);
}

function filterTable() {
    if (!dataTable) return;
    var allRows = dataTable.rows().nodes();
    $(allRows).each(function() {
        var row = dataTable.row(this);
        var d = row.data();
        if (d && d.code) {
            $(this).toggle(selectedCountries.has(d.code));
        }
    });
}

// ========== CSV导出 ==========

function csvEscape(val) {
    if (val == null) return '';
    var s = String(val).replace(/"/g, '""');
    return '"' + s + '"';
}

function exportCSV() {
    if (!dataTable) return;

    // 获取当前列顺序
    var colOrder = dataTable.colReorder ? dataTable.colReorder.order() : [];
    var cols = dataTable.settings()[0].aoColumns;
    if (colOrder.length === 0) {
        for (var i = 0; i < cols.length; i++) colOrder.push(i);
    }

    // 单元数据映射：DataTables列序号 → allData字段路径
    var rawPaths = [
        function(c) { return c.nameZh + ' ' + c.nameEn; },
        function(c) { return c.population; },
        function(c) { return c.gdpPerCapita; },
        function(c) { return c.gdpTotal; },
        function(c) { return c.meat.total; },
        function(c) { return c.meat.pig; },
        function(c) { return c.meat.beef; },
        function(c) { return c.meat.sheep; },
        function(c) { return c.meat.poultry; },
        function(c) { return c.meat.other; },
        function(c) { return c.meat.fish; },
        function(c) { return c.milk; },
        function(c) { return c.egg; },
        function(c) { return c.vegetable; },
        function(c) { return c.fruit; },
        function(c) { return c.lifeExpectancy; },
        function(c) { return c.energy; }
    ];

    // 创建代码到原始数据的映射
    var dataMap = {};
    allData.forEach(function(c) { dataMap[c.code] = c; });

    // 构建表头（直接从thead的th元素读取，兼容ColReorder）
    var headers = [];
    var paths = [];
    var $thElements = $('#data-table thead th');
    for (var j = 0; j < colOrder.length; j++) {
        var idx = colOrder[j];
        var th = $thElements.eq(j).text().replace(/[\n\r]/g, '').trim();
        headers.push(csvEscape(th));
        paths.push(rawPaths[idx]);
    }

    // 构建行（仅被选中的国家）
    var rows = [];
    allData.forEach(function(c) {
        if (c.code === 'OWID_WRL') return;
        if (!selectedCountries.has(c.code)) return;
        var row = [];
        for (var k = 0; k < paths.length; k++) {
            var val = paths[k](c);
            if (val == null || val === '') val = '';
            else if (typeof val === 'number') val = val.toFixed(4).replace(/\.?0+$/, '');
            row.push(csvEscape(val));
        }
        rows.push(row.join(','));
    });

    if (rows.length === 0) {
        alert('没有可导出的数据');
        return;
    }

    var BOM = '\uFEFF';
    var csv = BOM + headers.join(',') + '\n' + rows.join('\n');

    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = '人均消费数据_' + new Date().toISOString().slice(0, 10) + '.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    console.log('CSV导出完成', rows.length, '条记录');
}

// ========== 数字格式化 ==========

function formatNumber(num) {
    if (num === null || num === undefined || isNaN(num)) return '<span class="missing-data">—</span>';
    var n = Math.abs(num);
    if (n >= 1e15) return (num / 1e15).toFixed(2) + ' 亿亿';
    if (n >= 1e11) return (num / 1e11).toFixed(2) + ' 万亿';
    if (n >= 1e8)  return (num / 1e8).toFixed(2) + ' 亿';
    if (n >= 1e4)  return (num / 1e4).toFixed(2) + ' 万';
    if (n >= 1000) return num.toLocaleString('zh-CN', { maximumFractionDigits: 2 });
    return num.toFixed(2);
}

function formatGDP(num) {
    if (num === null || num === undefined || isNaN(num)) return '<span class="missing-data">—</span>';
    var n = Math.abs(num);
    if (n >= 1e15) return (num / 1e15).toFixed(2) + ' 亿亿';
    if (n >= 1e11) return (num / 1e11).toFixed(2) + ' 万亿';
    if (n >= 1e8)  return (num / 1e8).toFixed(2) + ' 亿';
    if (n >= 1e4)  return (num / 1e4).toFixed(2) + ' 万';
    if (n >= 1000) return num.toLocaleString('zh-CN', { maximumFractionDigits: 0 });
    return num.toFixed(2);
}
