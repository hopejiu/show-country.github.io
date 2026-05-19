#!/usr/bin/env python3
"""
人均消费数据展示面板 - 数据处理脚本
处理来自 Our World in Data 的数据，生成前端所需的 JSON 格式
消费数据优先使用2023年，缺失则回退到2022、2021、2020，仍无数据则置为0
"""

import csv
import json
import os
from datetime import datetime

# 数据文件路径
DATA_DIR = 'data'
OUTPUT_FILE = 'web/data/processed-data.json'
COUNTRY_MAPPING_FILE = 'country_mapping.json'

# 消费数据回退年份（优先2023，然后2022、2021、2020）
FALLBACK_YEARS = [2023, 2022, 2021, 2020]


def read_csv_file_fallback(file_path):
    """读取CSV文件，按FALLBACK_YEARS优先级获取每个国家最新可用数据
    返回 {code: {'row': row, 'year': year}} 
    """
    all_rows = []  # [(code, year, row), ...]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row_year = int(row['Year'])
                    code = row['Code']
                    if code and row_year in FALLBACK_YEARS:
                        all_rows.append((code, row_year, row))
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"警告: 文件 {file_path} 未找到")
        return {}

    # 按国家分组，优先取最近的年份
    result = {}
    for code, year, row in all_rows:
        if code not in result or year > result[code]['year']:
            result[code] = {'row': row, 'year': year}
    return result


def read_csv_file_single(file_path, year):
    """读取CSV文件并筛选指定年份的数据"""
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row_year = int(row['Year'])
                    if row_year == year:
                        code = row['Code']
                        if code:
                            data[code] = row
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"警告: 文件 {file_path} 未找到")
    return data


def load_country_mapping():
    """加载中英文国家名称映射"""
    try:
        with open(COUNTRY_MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: 国家映射文件 {COUNTRY_MAPPING_FILE} 未找到")
        return {}


def safe_float(value, default=None):
    """安全转换为浮点数"""
    if not value or value.strip() == '':
        return default
    try:
        return float(value)
    except ValueError:
        return default


def safe_int(value, default=None):
    """安全转换为整数"""
    if not value or value.strip() == '':
        return default
    try:
        return int(float(value))
    except ValueError:
        return default


def process_data():
    """处理所有数据并生成JSON"""
    print("开始处理数据...")

    # 加载国家映射
    country_mapping = load_country_mapping()
    print(f"加载了 {len(country_mapping)} 个国家映射")

    # 读取GDP数据（2022年）
    print("读取GDP数据（2022年）...")
    gdp_data = read_csv_file_single(
        os.path.join(DATA_DIR, 'gdp-per-capita-maddison-project-database', 'gdp-per-capita-maddison-project-database.csv'),
        2022)
    print(f"读取了 {len(gdp_data)} 个国家的GDP数据")

    # 读取人口数据（2023年）
    print("读取人口数据（2023年）...")
    population_data = read_csv_file_single(
        os.path.join(DATA_DIR, 'population-with-un-projections', 'population-with-un-projections.csv'),
        2023)
    print(f"读取了 {len(population_data)} 个国家的人口数据")

    # 读取消费数据（带回退机制）
    print("读取肉类和水产数据（回退到2020年）...")
    meat_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'per-capita-meat-type', 'per-capita-meat-type.csv'))
    print(f"读取了 {len(meat_data)} 个国家的肉类数据")
    # 统计回退年份
    year_stats = {}
    for code, info in meat_data.items():
        y = info['year']
        year_stats[y] = year_stats.get(y, 0) + 1
    for y in sorted(year_stats.keys()):
        print(f"  使用{y}年数据: {year_stats[y]} 个国家")

    print("读取奶类数据（回退到2020年）...")
    milk_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'per-capita-milk-consumption', 'per-capita-milk-consumption.csv'))
    print(f"读取了 {len(milk_data)} 个国家的奶类数据")

    print("读取蛋类数据（回退到2020年）...")
    egg_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'per-capita-egg-consumption-kilograms-per-year', 'per-capita-egg-consumption-kilograms-per-year.csv'))
    print(f"读取了 {len(egg_data)} 个国家的蛋类数据")

    print("读取蔬菜数据（回退到2020年）...")
    vegetable_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'vegetable-consumption-per-capita', 'vegetable-consumption-per-capita.csv'))
    print(f"读取了 {len(vegetable_data)} 个国家的蔬菜数据")

    print("读取水果数据（回退到2020年）...")
    fruit_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'fruit-consumption-per-capita', 'fruit-consumption-per-capita.csv'))
    print(f"读取了 {len(fruit_data)} 个国家的水果数据")

    print("读取预期寿命数据（回退到2020年）...")
    life_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'life-expectancy', 'life-expectancy.csv'))
    print(f"读取了 {len(life_data)} 个国家的预期寿命数据")

    print("读取人均能源数据（回退到2020年）...")
    energy_data = read_csv_file_fallback(
        os.path.join(DATA_DIR, 'per-capita-energy-use', 'per-capita-energy-use.csv'))
    print(f"读取了 {len(energy_data)} 个国家的人均能源数据")

    # 获取所有独特的国家代码
    all_codes = set()
    all_codes.update(gdp_data.keys())
    all_codes.update(population_data.keys())
    all_codes.update(meat_data.keys())
    all_codes.update(milk_data.keys())
    all_codes.update(egg_data.keys())
    all_codes.update(vegetable_data.keys())
    all_codes.update(fruit_data.keys())
    all_codes.update(life_data.keys())
    all_codes.update(energy_data.keys())

    print(f"总共找到 {len(all_codes)} 个国家/地区")

    # 找出有回退数据的国家
    fallback_countries = set()
    for code in all_codes:
        if code in meat_data and meat_data[code]['year'] < 2023:
            fallback_countries.add(code)

    # 处理每个国家的数据
    countries = []
    missing_data_countries = {}
    for code in sorted(all_codes):
        # 跳过空代码
        if not code or code.strip() == '':
            continue

        # 获取国家名称
        gdp_info = gdp_data.get(code, {})
        population_info = population_data.get(code, {})

        # 获取英文名称
        name_en = gdp_info.get('Entity') or population_info.get('Entity') or code
        # 如果population数据中有Entity，优先使用
        if code in population_data:
            name_en = population_data[code].get('Entity', name_en)

        # 获取中文名称
        name_zh = country_mapping.get(code, {}).get('zh', name_en)

        # 获取人口数据
        population = safe_int(population_info.get('Population'))

        # 获取GDP数据
        gdp_per_capita = safe_float(gdp_info.get('GDP per capita'))

        # 计算GDP总量
        gdp_total = 0
        if gdp_per_capita is not None and population is not None:
            gdp_total = gdp_per_capita * population

        # 获取肉类数据（带fallback）
        meat_info_res = meat_data.get(code, {})
        meat_row = meat_info_res.get('row', {}) if meat_info_res else {}
        meat_year = meat_info_res.get('year', 0) if meat_info_res else 0

        meat_pig = safe_float(meat_row.get('Pork'), 0)
        meat_beef = safe_float(meat_row.get('Beef and buffalo'), 0)
        meat_sheep = safe_float(meat_row.get('Sheep and goat'), 0)
        meat_poultry = safe_float(meat_row.get('Poultry'), 0)
        meat_other = safe_float(meat_row.get('Other meats'), 0)
        meat_fish = safe_float(meat_row.get('Fish and seafood'), 0)
        meat_total = meat_pig + meat_beef + meat_sheep + meat_poultry + meat_other + meat_fish

        # 获取其他消费数据（带fallback）
        milk_info = milk_data.get(code, {})
        milk_row = milk_info.get('row', {}) if milk_info else {}
        milk = safe_float(milk_row.get('Per capita consumption of milk, excluding butter'), 0)

        egg_info = egg_data.get(code, {})
        egg_row = egg_info.get('row', {}) if egg_info else {}
        egg = safe_float(egg_row.get('Egg supply per person'), 0)

        vegetable_info = vegetable_data.get(code, {})
        vegetable_row = vegetable_info.get('row', {}) if vegetable_info else {}
        vegetable = safe_float(vegetable_row.get('Vegetable supply per person'), 0)

        fruit_info = fruit_data.get(code, {})
        fruit_row = fruit_info.get('row', {}) if fruit_info else {}
        fruit = safe_float(fruit_row.get('Fruit supply per person'), 0)

        # 获取预期寿命和能源数据
        life_info = life_data.get(code, {})
        life_row = life_info.get('row', {}) if life_info else {}
        life_expectancy = safe_float(life_row.get('Life expectancy'), 0)

        energy_info = energy_data.get(code, {})
        energy_row = energy_info.get('row', {}) if energy_info else {}
        energy = safe_float(energy_row.get('Per capita energy consumption'), 0)

        # 记录数据年份信息
        if code in fallback_countries:
            missing_data_countries[code] = {
                'nameZh': name_zh,
                'meatYear': meat_year,
            }

        # 创建国家数据对象
        country = {
            'code': code,
            'nameEn': name_en,
            'nameZh': name_zh,
            'population': population or 0,
            'gdpPerCapita': gdp_per_capita or 0,
            'gdpTotal': gdp_total,
            'meat': {
                'total': meat_total,
                'pig': meat_pig,
                'beef': meat_beef,
                'sheep': meat_sheep,
                'poultry': meat_poultry,
                'other': meat_other,
                'fish': meat_fish
            },
            'milk': milk,
            'egg': egg,
            'vegetable': vegetable,
            'fruit': fruit,
            'lifeExpectancy': life_expectancy,
            'energy': energy
        }

        countries.append(country)

    # 打印使用了回退数据的国家
    print(f"\n消费数据未使用2023年的国家（使用较早年份数据）: {len(missing_data_countries)} 个")
    for code, info in sorted(missing_data_countries.items()):
        print(f"  {info['nameZh']} ({code}): 肉类使用{info['meatYear']}年数据")

    # 按GDP总量排序（降序）
    countries.sort(key=lambda x: x.get('gdpTotal') or 0, reverse=True)

    # 创建输出数据
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'gdp_year': 2022,
            'other_year': 2023,
            'total_countries': len(countries),
            'note': 'GDP数据基于购买力平价（PPP），单位为国际元（2011年价格）。消费数据优先2023年，缺失则回退至2020年。'
        },
        'countries': countries
    }

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # 写入JSON文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n数据处理完成！")
    print(f"共处理了 {len(countries)} 个国家/地区")
    print(f"输出文件: {OUTPUT_FILE}")

    # 显示前5个国家的数据
    print("\n前5个国家的数据：")
    for i, country in enumerate(countries[:5]):
        print(f"{i+1}. {country['nameZh']} ({country['code']})")
        print(f"   人口: {country['population']:,}")
        print(f"   人均GDP: {country['gdpPerCapita']:,} 国际元")
        print(f"   GDP总量: {country['gdpTotal']:,.0f} 国际元")
        meat_total = country['meat']['total']
        meat_total_str = f"{meat_total:.1f}" if meat_total is not None else "N/A"
        print(f"   肉类总量: {meat_total_str} kg/人/年")
        print()


if __name__ == '__main__':
    process_data()
