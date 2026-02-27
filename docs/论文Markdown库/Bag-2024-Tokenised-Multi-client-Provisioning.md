# Xray - Bag 2024 - Tokenised Multi-client Provisioning

## 文档信息
- 标题: Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy
- 作者: Arnab Bag, Sikhar Patranabis, Debdeep Mukhopadhyay
- 会议: ASIA CCS 2024
- DOI: `10.1145/3634737.3657018`
- 来源 PDF: `/Users/cyan/code/paper/ref-thesis/Bag 等 - 2024 - Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Priv.pdf`
- 抽取方法: `ljg-xray-paper` 结构化解构（非全文转存）

---

## 【1. 核心痛点】
- 一句话定义: 如何在**动态** SSE 中同时支持**多客户端并发查询**、**前向+后向隐私**与**可落地效率**，且不被多客户端交互泄露击穿。
- 前人困境:
  - ODXT 等 SOTA 动态方案主要是单客户端（SRSW）。
  - 把 ODXT 直接扩展到多客户端（MC-ODXT）会暴露 cross-term 访问模式。
  - 该泄露可被“半诚实服务器 + 串通客户端”利用，恢复查询关键词（论文给出攻击流程与实验）。

## 【2. 解题机制】
- 核心直觉: 不是让每个客户端持密钥，而是引入可信 gate-keeper 做**令牌化供给**；同时让 XSet 访问“看起来每次都不一样”，切断可链接性。
- 关键步骤:
  1. Tokenised multi-client provisioning:
     - 采用 MRSW 架构，只有 gate-keeper 更新数据库并生成搜索令牌。
     - 客户端通过 OPRF 交互拿到搜索令牌，不暴露查询关键词，也不持有主密钥。
  2. Cross-term leakage mitigation:
     - 用 RBF（Redundant Bloom Filter）替代直接确定性地址访问。
     - 更新阶段写入冗余地址；搜索阶段随机选子集地址验证，打散重复访问模式。

## 【3. 创新增量】
- 对比 SOTA:
  - 相比 ODXT: 从单客户端动态检索，推进到多客户端（MRSW）动态合取查询。
  - 相比“直接多客户端扩展”: 明确修复 cross-term 可利用泄露。
  - 保持工程可用性: 线性存储、子线性搜索，在真实数据上性能接近静态合取 SSE。
- 新拼图:
  - 给“动态 + 多客户端 + 合取查询”这一长期断层组合，补上可执行构造（Nomos）。
  - 证明了多客户端不是简单“套壳扩展”，而要重做泄露面设计。

## 【4. 批判性边界】
- 隐形假设:
  - gate-keeper 是可信实体，且承担集中式令牌发放与更新权。
  - 服务器与客户端按半诚实模型执行（论文重点处理串通导致的 cross-term 泄露，但整体仍在该模型下分析）。
- 未解之谜:
  - 主要给出 MRSW，不是 MRMW（多写者）完整方案。
  - 对 s-term 与更复杂泄露面的系统性缓解仍留后续工作。
  - 仍以索引级检索为核心，完整文档检索链路的通用化不是主目标。

## 【5. 一言以蔽之】
- 餐巾纸公式:

```text
Practical Multi-client Dynamic SSE
= Tokenized Provisioning (OPRF + Gatekeeper)
+ Access Decorrelation (RBF over XSet)
```

- 餐巾纸图:

```text
+-----------+      token request      +-------------+
| Client Ci | <---------------------> | Gatekeeper G|
+-----------+        (OPRF)           +-------------+
      |                                      |
      | search token                         | update only
      v                                      v
+---------------------------------------------------------+
| Server S: EDB = TSet + XSet(RBF-backed)                 |
| 1) use TSet to enumerate candidates                      |
| 2) use randomized RBF lookups for cross-term checks      |
+---------------------------------------------------------+
      |
      v
  encrypted result
```

## 逻辑结构图（ASCII）

```text
Problem
  |
  +--> ODXT is SRSW only
  |
  +--> Trivial MC extension leaks cross-term access
  |         |
  |         +--> query recovery attack (colluding client + server)
  |
  +--> Need dynamic + multi-client + privacy + efficiency
            |
            +--> Nomos
                  |
                  +--> OPRF tokenized provisioning via gatekeeper
                  |
                  +--> RBF-based decorrelated XSet access
                  |
                  +--> linear storage + sublinear search (practical)
```

## 可直接复用到论文的结论句
- “该工作揭示了多客户端动态 SSE 的关键难点不在功能叠加，而在 cross-term 访问模式泄露的可链接性控制。”
- “通过 gate-keeper 令牌化供给与 RBF 访问去关联，Nomos 在 MRSW 场景下实现了动态合取检索与隐私约束的工程平衡。”
- “该路线为本文后续在可验证语义下扩展多客户端动态 SSE 提供了现实基线与接口参照。”
