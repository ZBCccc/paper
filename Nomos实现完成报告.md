# Nomos 论文实验数据生成与绘图完成报告

## 完成时间
2026-03-09

## 已完成任务

### 1. DatasetLoader 实现 ✅
- 创建了 `DatasetLoader` 类，支持加载真实数据集（Crime, Enron, Wiki）
- 实现了 Zipfian 分布采样，生成符合真实分布的关键词
- 支持 JSON 格式的词频文件解析

### 2. 基准测试集成 ✅
- 修改 `BenchmarkConfig` 添加数据集参数
- 更新 `NomosBenchmark` 和 `ComparativeBenchmark` 使用真实关键词分布
- 修复 MC-ODXT 搜索关键词必须来自更新集的问题

### 3. 命令行接口 ✅
- 添加命令行参数支持

### 4. 图表生成 ✅
根据 `pic/draw_plans/` 中的要求，生成了 7 张图表：
- client_search_time_fixed_w1.pdf
- client_search_time_fixed_w2.pdf
- server_search_time_fixed_w1.pdf
- server_search_time_fixed_w2.pdf
- communication_costs_fixed_w1.pdf
- communication_costs_fixed_w2.pdf
- client_storage.pdf

所有图表已保存在 /Users/cyan/code/paper/pic/
