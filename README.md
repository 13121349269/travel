# 山西 · 运城全域旅游攻略

一套纯前端、免Key、打开即用的运城全域旅游工具包。

## 页面

| 页面 | 内容 |
|---|---|
| `index.html` | 站点首页导航 |
| `map.html` | **运城55家A级景区地图标注**（4A×24 / 3A×19 / 2A×9 / 1A×1）+ 美食街、住宿圈、网红点，共70个点位，含门票/评分/真人评价/高德导航 |
| `shanxi.html` | 山西省451家A级景区总表，按11地市分组，支持筛选 |
| `guide.html` | 运城食宿攻略：3住宿圈7家酒店、5条小吃街、10道美食、14个网红打卡点 |

## 技术

- [Leaflet.js](https://github.com/Leaflet/Leaflet) + [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)（GitHub 开源）
- 高德地图瓦片（GCJ-02），免 API Key
- 纯静态 HTML，GitHub Pages 部署

## 线上地址

**https://lovesummer.me/**

## 数据来源

运城市文化和旅游局、山西省文旅厅官方名录（2025-2026）；携程、同程等多平台门票与评分核实。
全国5A/4A全量图层：[China Top Attractions](https://chinatopattractions.com/china-attractions-dataset/) 公开数据集（1,310条，WGS-84坐标，2026-08核验，已转GCJ-02）。
全国A级景区总量口径：文化和旅游部《2025年文化和旅游发展统计公报》（2025年末16,994个）。

## 已知限制

- 小众景区坐标为乡镇级近似定位
- 少数未查到官方票价的小景区标注【待核实】
- 万荣东岳庙（1A）与飞云楼（3A）同址（飞云楼即东岳庙主楼）
