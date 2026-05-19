#!/usr/bin/env python3
"""
数据处理脚本测试
"""

import os
import sys
import json
import pytest

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_data import (
    read_csv_file_single,
    safe_float,
    safe_int,
    load_country_mapping
)

class TestDataProcessing:
    """数据处理测试类"""
    
    def test_safe_float_valid(self):
        """测试safe_float函数 - 有效值"""
        assert safe_float("123.45") == 123.45
        assert safe_float("0") == 0.0
        assert safe_float("-123.45") == -123.45
    
    def test_safe_float_invalid(self):
        """测试safe_float函数 - 无效值"""
        assert safe_float("") is None
        assert safe_float(None) is None
        assert safe_float("abc") is None
        assert safe_float("N/A") is None
    
    def test_safe_float_default(self):
        """测试safe_float函数 - 默认值"""
        assert safe_float("", 0.0) == 0.0
        assert safe_float(None, -1.0) == -1.0
    
    def test_safe_int_valid(self):
        """测试safe_int函数 - 有效值"""
        assert safe_int("123") == 123
        assert safe_int("0") == 0
        assert safe_int("-123") == -123
        assert safe_int("123.45") == 123
    
    def test_safe_int_invalid(self):
        """测试safe_int函数 - 无效值"""
        assert safe_int("") is None
        assert safe_int(None) is None
        assert safe_int("abc") is None
    
    def test_safe_int_default(self):
        """测试safe_int函数 - 默认值"""
        assert safe_int("", 0) == 0
        assert safe_int(None, -1) == -1
    
    def test_load_country_mapping(self):
        """测试国家映射加载"""
        mapping = load_country_mapping()
        assert isinstance(mapping, dict)
        assert len(mapping) > 0
        
        # 检查一些已知的国家
        assert "CHN" in mapping
        assert "USA" in mapping
        assert "JPN" in mapping
        
        # 检查映射结构
        assert "en" in mapping["CHN"]
        assert "zh" in mapping["CHN"]
        assert mapping["CHN"]["zh"] == "中国"
    
    def test_read_csv_file(self):
        """测试CSV文件读取"""
        # 测试GDP数据文件
        gdp_file = "data/gdp-per-capita-maddison-project-database/gdp-per-capita-maddison-project-database.csv"
        if os.path.exists(gdp_file):
            data = read_csv_file_single(gdp_file, 2022)
            assert isinstance(data, dict)
            # 应该有一些数据
            assert len(data) > 0
    
    def test_processed_data_format(self):
        """测试处理后的数据格式"""
        output_file = "assets/processed-data.json"
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查顶层结构
            assert "metadata" in data
            assert "countries" in data
            
            # 检查元数据
            metadata = data["metadata"]
            assert "generated_at" in metadata
            assert "gdp_year" in metadata
            assert "other_year" in metadata
            assert "total_countries" in metadata
            
            # 检查国家数据
            countries = data["countries"]
            assert isinstance(countries, list)
            assert len(countries) > 0
            
            # 检查第一个国家的数据结构
            first_country = countries[0]
            required_fields = [
                "code", "nameEn", "nameZh", "population",
                "gdpPerCapita", "gdpTotal", "meat", "milk",
                "egg", "vegetable", "fruit", "lifeExpectancy", "energy"
            ]
            for field in required_fields:
                assert field in first_country, f"缺少字段: {field}"
            
            # 检查肉类数据结构
            meat = first_country["meat"]
            meat_fields = ["total", "pig", "beef", "sheep", "poultry", "other", "fish"]
            for field in meat_fields:
                assert field in meat, f"肉类数据缺少字段: {field}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])