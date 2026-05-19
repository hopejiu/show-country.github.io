#!/usr/bin/env python3
"""
人均消费数据展示面板 - 数据处理脚本
处理来自 Our World in Data 的数据，生成前端所需的 JSON 格式
"""

import csv
import json
import os
from datetime import datetime

# 数据文件路径
DATA_DIR = 'data'
OUTPUT_FILE = 'web/data/processed-data.json'
COUNTRY_MAPPING_FILE = 'country_mapping.json'

def read_csv_file(file_path, year=2023):
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
                        if code:  # 确保有国家代码
                            data[code] = row
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"警告: 文件 {file_path} 未找到")
    return data

def read_gdp_data(year=2022):
    """读取GDP数据（使用2022年数据）"""
    file_path = os.path.join(DATA_DIR, 'gdp-per-capita-maddison-project-database', 'gdp-per-capita-maddison-project-database.csv')
    return read_csv_file(file_path, year)

def read_population_data(year=2023):
    """读取人口数据"""
    file_path = os.path.join(DATA_DIR, 'population-with-un-projections', 'population-with-un-projections.csv')
    return read_csv_file(file_path, year)

def read_meat_data(year=2023):
    """读取肉类和水产消费数据"""
    file_path = os.path.join(DATA_DIR, 'per-capita-meat-type', 'per-capita-meat-type.csv')
    return read_csv_file(file_path, year)

def read_milk_data(year=2023):
    """读取奶类消费数据"""
    file_path = os.path.join(DATA_DIR, 'per-capita-milk-consumption', 'per-capita-milk-consumption.csv')
    return read_csv_file(file_path, year)

def read_egg_data(year=2023):
    """读取蛋类消费数据"""
    file_path = os.path.join(DATA_DIR, 'per-capita-egg-consumption-kilograms-per-year', 'per-capita-egg-consumption-kilograms-per-year.csv')
    return read_csv_file(file_path, year)

def read_vegetable_data(year=2023):
    """读取蔬菜消费数据"""
    file_path = os.path.join(DATA_DIR, 'vegetable-consumption-per-capita', 'vegetable-consumption-per-capita.csv')
    return read_csv_file(file_path, year)

def read_fruit_data(year=2023):
    """读取消费数据"""
    file_path = os.path.join(DATA_DIR, 'fruit-consumption-per-capita', 'fruit-consumption-per-capita.csv')
    return read_csv_file(file_path, year)

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
    
    # 读取所有数据
    print("读取GDP数据...")
    gdp_data = read_gdp_data(2022)
    print(f"读取了 {len(gdp_data)} 个国家的GDP数据")
    
    print("读取人口数据...")
    population_data = read_population_data(2023)
    print(f"读取了 {len(population_data)} 个国家的人口数据")
    
    print("读取肉类和水产数据...")
    meat_data = read_meat_data(2023)
    print(f"读取了 {len(meat_data)} 个国家的肉类数据")
    
    print("读取奶类数据...")
    milk_data = read_milk_data(2023)
    print(f"读取了 {len(milk_data)} 个国家的奶类数据")
    
    print("读取蛋类数据...")
    egg_data = read_egg_data(2023)
    print(f"读取了 {len(egg_data)} 个国家的蛋类数据")
    
    print("读取蔬菜数据...")
    vegetable_data = read_vegetable_data(2023)
    print(f"读取了 {len(vegetable_data)} 个国家的蔬菜数据")
    
    print("读取消费数据...")
    fruit_data = read_fruit_data(2023)
    print(f"读取了 {len(fruit_data)} 个国家的水果数据")
    
    # 获取所有独特的国家代码
    all_codes = set()
    all_codes.update(gdp_data.keys())
    all_codes.update(population_data.keys())
    all_codes.update(meat_data.keys())
    all_codes.update(milk_data.keys())
    all_codes.update(egg_data.keys())
    all_codes.update(vegetable_data.keys())
    all_codes.update(fruit_data.keys())
    
    print(f"总共找到 {len(all_codes)} 个国家/地区")
    
    # 处理每个国家的数据
    countries = []
    for code in sorted(all_codes):
        # 跳过空代码
        if not code or code.strip() == '':
            continue
        
        # 获取国家名称
        gdp_info = gdp_data.get(code, {})
        population_info = population_data.get(code, {})
        meat_info = meat_data.get(code, {})
        
        # 获取英文名称
        name_en = gdp_info.get('Entity') or population_info.get('Entity') or meat_info.get('Entity') or code
        
        # 获取中文名称
        name_zh = country_mapping.get(code, {}).get('zh', name_en)
        
        # 获取人口数据
        population = safe_int(population_info.get('Population'))
        
        # 获取GDP数据
        gdp_per_capita = safe_float(gdp_info.get('GDP per capita'))
        
        # 计算GDP总量
        gdp_total = None
        if gdp_per_capita is not None and population is not None:
            gdp_total = gdp_per_capita * population
        
        # 获取肉类数据
        meat_total = None
        meat_pig = safe_float(meat_info.get('Pork'))
        meat_beef = safe_float(meat_info.get('Beef and buffalo'))
        meat_sheep = safe_float(meat_info.get('Sheep and goat'))
        meat_poultry = safe_float(meat_info.get('Poultry'))
        meat_other = safe_float(meat_info.get('Other meats'))
        meat_fish = safe_float(meat_info.get('Fish and seafood'))
        
        # 计算肉类总量
        meat_values = [v for v in [meat_pig, meat_beef, meat_sheep, meat_poultry, meat_other, meat_fish] if v is not None]
        if meat_values:
            meat_total = sum(meat_values)
        
        # 获取其他消费数据
        milk = safe_float(milk_data.get(code, {}).get('Per capita consumption of milk, excluding butter'))
        egg = safe_float(egg_data.get(code, {}).get('Egg supply per person'))
        vegetable = safe_float(vegetable_data.get(code, {}).get('Vegetable supply per person'))
        fruit = safe_float(fruit_data.get(code, {}).get('Fruit supply per person'))
        
        # 创建国家数据对象
        country = {
            'code': code,
            'nameEn': name_en,
            'nameZh': name_zh,
            'population': population,
            'gdpPerCapita': gdp_per_capita,
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
            'fruit': fruit
        }
        
        countries.append(country)
    
    # 按GDP总量排序（降序）
    countries.sort(key=lambda x: x.get('gdpTotal') or 0, reverse=True)
    
    # 创建输出数据
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'gdp_year': 2022,
            'other_year': 2023,
            'total_countries': len(countries),
            'note': 'GDP数据基于购买力平价（PPP），单位为国际元（2011年价格）'
        },
        'countries': countries
    }
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 写入JSON文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据处理完成！")
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