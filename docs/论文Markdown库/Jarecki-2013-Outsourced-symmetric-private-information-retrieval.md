# Xray - Jarecki 2013 - Outsourced Symmetric PIR

## 文档信息
- 标题: Outsourced Symmetric Private Information Retrieval
- 作者: Stanislaw Jarecki, Charanjit Jutla, Hugo Krawczyk, Marcel Rosu, Michael Steiner
- 会议: ACM CCS 2013
- DOI: `10.1145/2508859.2516730`
- 来源 PDF: `/Users/cyan/code/paper/ref-thesis/Jarecki 等 - 2013 - Outsourced symmetric private information retrieval.pdf`
- 抽取方法: `ljg-xray-paper` 结构化解构（非全文转存）

---

## 【1. 核心痛点】
- 一句话定义: 在可搜索加密外包场景中，如何同时满足“多客户端授权搜索”和“客户端查询对数据拥有者也保密”。
- 前人困境:
  - 传统 SSE 主要是数据拥有者自己搜（单客户端）。
  - 让第三方客户端可搜后，授权可做，但查询常会暴露给数据拥有者。
  - 布尔查询下，直接改造 OXT 会遇到令牌数依赖数据、可验证授权与隐私并存难题。

## 【2. 解题机制】
- 核心直觉: 把“能搜”与“知道你搜什么”分离。数据拥有者只做策略授权和令牌协作，不直接拿到查询值。
- 关键步骤:
  1. MC-OXT（多客户端）:
     - 基于 OXT 扩展到多客户端授权搜索。
     - 客户端拿到可验证授权令牌，服务端可验真，防伪造。
  2. OSPIR-OXT（查询对拥有者私密）:
     - 引入 OPRF / shared-OPRF，使查询值在令牌生成时对拥有者保持隐藏。
     - 拥有者只看到最小策略相关信息（如属性类别），不见具体值。

## 【3. 创新增量】
- 对比 SOTA:
  - 相比单客户端 OXT: 支持多客户端布尔查询授权（MC-SSE）。
  - 相比仅多客户端授权: 进一步实现“对拥有者也私密”的 OSPIR。
  - 在维持功能增强的同时，保持接近 OXT 的性能级别（论文给出实现与开销分析）。
- 新拼图:
  - 把 SSE 从“服务器不知查询”推进到“服务器和数据拥有者都不知查询值”的更强外包模型。
  - 提供可落地的协议组合路径：OXT + OPRF + 可验证授权。

## 【4. 批判性边界】
- 隐形假设:
  - 主要威胁模型中服务器与拥有者不串通（non-colluding）。
  - 拥有者在策略执行与令牌发放过程中被视为可执行协议但受模型约束。
- 未解之谜:
  - 若拥有者与服务器串通，隐私边界会显著收缩。
  - 强对抗部署下的系统复杂度、工程运维成本没有完全解决。
  - 后续动态更新与更复杂策略组合仍需进一步优化。

## 【5. 一言以蔽之】
- 餐巾纸公式:

```text
OSPIR-SSE = OXT-style Searchability
          + Multi-client Authorization
          + Query Privacy from Data Owner (via OPRF)
```

- 餐巾纸图:

```text
+-----------+     private token protocol     +---------------+
| Client C  | <----------------------------> | Data Owner D  |
+-----------+                                +---------------+
      |                                               |
      | authorized search token                       | policy check only
      v                                               v
+--------------------------------------------------------------+
| Outsourced Server E : encrypted index / data                 |
| - verifies token validity                                    |
| - executes boolean keyword search                            |
+--------------------------------------------------------------+
      |
      v
  matching encrypted records to C
```

## 逻辑结构图（ASCII）

```text
Need outsourced search
  |
  +--> SSE gives server-side privacy
  |
  +--> Multi-client access required
  |      |
  |      +--> MC-OXT (authorized client search)
  |
  +--> Client query should be hidden from owner too
         |
         +--> OSPIR-OXT (OPRF-based query blinding)
                 |
                 +--> policy-compliant + owner-private querying
```

## 可直接复用到论文的结论句
- “该工作将可搜索加密从单客户端扩展到多客户端授权场景，并进一步提出了对数据拥有者隐藏查询值的 OSPIR 模型。”
- “其关键方法是将 OXT 的高效检索骨架与 OPRF 型隐私令牌协作机制组合，实现策略可执行与查询隐私并存。”
- “该路线为后续‘多方参与、细粒度授权、可验证检索’的研究提供了重要协议分层思路。”
