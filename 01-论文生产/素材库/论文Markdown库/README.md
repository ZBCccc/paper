# 论文 Markdown 库

## 目录用途

本目录用于存放从 `ref-thesis/` PDF 抽取得到的 Markdown 文献稿，默认采用 `ljg-xray-paper` 方法论（结构化解构），便于：

1. 全文检索
2. 快速摘录与二次标注
3. 与论文写作系统联动

## 命名规范

- 格式：`作者-年份-标题关键词.md`
- 示例：`Bag-2024-Tokenised-Multi-client-Provisioning.md`
- 原始转储（可选备份）：`作者-年份-标题关键词.raw.md`

## 文档头信息规范

每个 Markdown 文件开头必须包含：

- 源 PDF 路径
- DOI（若有）
- 转换时间
- 提取质量说明

## 当前文件

- `Bag-2024-Tokenised-Multi-client-Provisioning.md`
- `Bag-2024-Tokenised-Multi-client-Provisioning.raw.md`
- `Jarecki-2013-Outsourced-symmetric-private-information-retrieval.md`
- `Jarecki-2013-Outsourced-symmetric-private-information-retrieval.raw.md`

## 默认抽取流程（Xray）

1. 从 PDF 抽取可读文本（技术步骤）
2. 按 `ljg-xray-paper` 框架输出：
   - 核心痛点
   - 解题机制
   - 创新增量
   - 批判性边界
   - 餐巾纸公式/图与 ASCII 逻辑结构图
3. 生成 Markdown 文档作为主文件
4. 原始全文转储仅作为 `.raw.md` 备份，不作为主阅读材料

## 技术命令（文本抽取）

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=/tmp/paper_raw.txt "<PDF路径>"
```

然后基于 Xray 框架结构化写入本目录的 `.md` 文件。
