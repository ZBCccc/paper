# 论文初稿 X 光解构

## 1. 核心痛点

- **一句话定义**：多用户多关键词 SSE 缺少对服务器搜索行为的可验证约束。
- **前人困境**：已有工作偏重隐私泄露控制，缺少低开销、工程可落地的双环节验证机制。

## 2. 解题机制

- **核心直觉**：把“搜索流程里最容易被作恶的两步”拆开验证。
- **关键步骤**：
  1. 用 MHT 替换资格检验中的概率结构，输出认证路径。
  2. 在更新阶段将承诺嵌入已有索引，约束结果返回阶段伪造行为。

## 3. 创新增量

- **对比现有方案**：
  - 资格检验：概率过滤 -> 可证明验证
  - 结果验证：独立验证索引 -> 嵌入式验证信息
- **新增拼图**：给多用户多关键词 SSE 增加“可追责的检索可信层”。

## 4. 批判性边界

- **隐形假设**：
  - 授权管理方可信
  - 未覆盖撤权用户与服务器串谋
- **未解问题**：
  - 高并发动态更新下的验证信息维护开销
  - 更复杂查询语义（析取/范围）下的可验证扩展

## 5. 一言以蔽之

- **餐巾纸公式**：

```text
Trusted Search = SSE Privacy + Verifiable Eligibility + Verifiable Result Return
```

- **餐巾纸图**：

```text
Query Q
  |
  v
Candidate via TSet
  |
  +--> Eligibility Check
  |      |-- old: probabilistic filter
  |      |-- new: MHT proof path
  |
  v
Result Assembly
  |-- old: unverifiable return
  |-- new: embedded commitment check
  v
User Verify -> Accept / Reject
```

---

**最后更新**：2026-02-13
**标签**：X光解构，研究主线，创新点
