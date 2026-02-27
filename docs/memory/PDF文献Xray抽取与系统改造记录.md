# PDF 文献 Xray 抽取与系统改造记录

## 记录目的

整理本轮从“论文内容补充”到“文献抽取流程改造”的完整操作，确保后续可复用、可追踪、可审计。

## 时间与范围

- 记录时间：2026-02-13
- 作用范围：
  1. 论文正文：`HUST-PhD-Thesis-Latex/body/chapter/bf.tex`
  2. 参考文献：`HUST-PhD-Thesis-Latex/ref/thesis.bib`
  3. 文献抽取库：`01-论文生产/素材库/论文Markdown库/`
  4. 工作系统规则：`CLAUDE.md`、`Instructions.md`、`控制面板.md`、`HUST-PhD-Thesis-Latex/CLAUDE.md`
  5. 方法流程：`01-论文生产/方法论/PDF转Markdown流程.md`

## 一、论文正文相关操作

### 1.1 补全 bf.tex 的算法与安全性段落

- 已完成 `bf.tex` 的 TODO 清零，补充内容包括：
  - MHT 替换 Bloom Filter 的结构设计
  - 初始化/搜索/验证算法流程与伪代码
  - 动态更新策略
  - 正确性、可验证性、隐私性分析
  - 本章小结

### 1.2 强化“协议接口与执行流程”并增加图示

- 参考 Bag 2024（Nomos）补充了 MRSW + tokenized provisioning 语义。
- 在 `bf.tex` 增加分阶段流程图（协议阶段 A/B/C/D）。

### 1.3 补充文献条目

- 在 `thesis.bib` 新增：`bag2024nomos`。

## 二、PDF 抽取流程改造

### 2.1 新建专用目录

- 新增目录：`01-论文生产/素材库/论文Markdown库/`
- 新增说明：`01-论文生产/素材库/论文Markdown库/README.md`

### 2.2 流程从“格式转换”升级为“Xray 抽取”

- 默认方法改为：`ljg-xray-paper`。
- 主产物从“全文清洗稿”变为“结构化解构稿”（核心痛点/机制/增量/边界/ASCII 图）。
- raw 全文转储改为可选备份：`*.raw.md`。

### 2.3 方法文档更新

- 更新文件：`01-论文生产/方法论/PDF转Markdown流程.md`
- 当前规范：
  1. 先做文本抽取
  2. 再按 Xray 框架输出主文档
  3. 可选保留 raw 备份

## 三、已完成的论文文献抽取

### 3.1 Bag 2024

- 主文件：`Bag-2024-Tokenised-Multi-client-Provisioning.md`（Xray）
- 备份：`Bag-2024-Tokenised-Multi-client-Provisioning.raw.md`
- DOI：`10.1145/3634737.3657018`

### 3.2 Jarecki 2013

- 主文件：`Jarecki-2013-Outsourced-symmetric-private-information-retrieval.md`（Xray）
- 备份：`Jarecki-2013-Outsourced-symmetric-private-information-retrieval.raw.md`
- DOI：`10.1145/2508859.2516730`

## 四、系统规则更新（已生效）

### 4.1 根目录规则

- `CLAUDE.md`：新增“论文 Markdown 库”与“默认 Xray 抽取规则”。
- `Instructions.md`：新增“论文 Markdown 文献库（默认 Xray）”和日常动作。
- `控制面板.md`：新增导航入口“论文 Markdown 库”。

### 4.2 子工程规则

- `HUST-PhD-Thesis-Latex/CLAUDE.md`：增加“优先使用论文Markdown库的 Xray 文档”说明。

## 五、当前工作流（稳定版）

1. 新增 PDF -> 文本抽取
2. 使用 `ljg-xray-paper` 生成 Xray 主文档
3. 必要时保存 raw 备份
4. 将可复用结论回填到章节/方法论/记忆库

## 六、风险与注意事项

1. 双栏 PDF 自动抽取仍可能存在断词/列拼接。
2. Xray 文档用于“理解与写作决策”，非逐字引用依据。
3. 精确引用与公式核对时必须回看原 PDF。

## 七、后续建议

1. 对 `ref-thesis/` 其余 PDF 按同一规则批处理。
2. 为每篇 Xray 文档补“可直接复用到论文”的 3-5 句模板。
3. 对高频引用论文建立“Xray + Bib + 章节映射”三联索引。

---

**最后更新**：2026-02-13
**标签**：记忆库，Xray抽取，PDF流程，系统改造，论文协作
