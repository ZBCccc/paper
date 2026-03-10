# CLAUDE.md - AI 总指南

面向学术论文研发的个人工作系统。建立长期记忆，复用方法论，沉淀素材，打通方法论与 LaTeX 工程的双向协作。

## 模型使用原则

- **论文内容撰写**（正文、证明、分析、改写）：`claude-opus-4-6`
- **Git 操作**（commit、status、log、push）：`claude-haiku-4-5-20251001`

## 三层文档结构

| 层级 | 路径 | 加载策略 |
|------|------|----------|
| 永远加载 | `CLAUDE.md` | 每次会话自动加载 |
| 自动加载 | `rules/` | 每次会话开始时读取全部文件 |
| 按需加载 | `docs/` | 用到时再读取 |

## rules/（自动加载）

| 文件 | 内容 |
|------|------|
| `rules/控制面板.md` | 章节状态、近期任务、快速导航 |
| `rules/角色与硬约束.md` | AI 角色定位（4 条）+ 论文表述硬约束（15 条） |
| `rules/工作流程.md` | 写作流程 + PDF 处理 + 日常执行规范 + 生命周期 |

## docs/（按需加载）

| 文件/目录 | 内容 |
|-----------|------|
| `docs/memory/` | 长期研究记忆（7 个记忆文件） |
| `docs/论文Markdown库/` | PDF 文献的 Xray Markdown 版本 |
| `docs/*.md` | 方法论、基础知识、研究流程等参考文档 |

## 不变项

- `HUST-PhD-Thesis-Latex/` — LaTeX 主工程
- `ref-thesis/` — 原始 PDF 文献
- `Nomos/` — 代码实现工程（C++11，RELIC/OpenSSL/GMP）
- `.claude/` — Claude Code 配置

## Nomos 代码工程（新增）

**位置**: `Nomos/`
**状态**: ✅ OPRF 协议完整实现（2026-03-08）

**快速命令**:
```bash
cd Nomos/build
cmake .. && cmake --build .
./tests/nomos_test  # 11/11 测试通过
./Nomos nomos-simplified  # 运行实验
```

**关键文档**:
- `Nomos/CLAUDE.md` - 代码工程详细指南
- `Nomos/OPRF实现总结.md` - OPRF 实现完整总结
- `Nomos/任务进度-2026-03-08.md` - 最新进度报告
- `OPRF盲化协议实现思路.md` - 实现思路（根目录）
- `Nomos方案实现分析.md` - 方案分析（根目录）

**实现状态**:
- ✅ Nomos Baseline (100%) - 完整 OPRF 四阶段协议
- ✅ OPRF Protocol (100%) - Client/Gatekeeper/Server 全部实现
- ✅ 测试覆盖 (100%) - 11/11 测试通过
- ⏳ Verifiable Nomos (90%)
- ⏳ MC-ODXT (20%)

## 系统健康检查

1. 找资料时，第一反应路径与实际路径是否一致？
2. 是否有长期未维护但仍占认知负担的目录？
3. 新增内容是否能在 10 秒内判断归档位置？

若任一项失败，说明系统结构需要调整。

---

**最后更新**：2026-03-08
**版本**：4.1（Nomos OPRF 协议完整实现，测试全部通过）
**论文版本**：4.0（三阶段盲审修复完成，64 个问题全部修复，就绪度 99%+）
