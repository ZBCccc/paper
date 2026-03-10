# OPRF 盲化协议实现思路

**日期**: 2026-03-07
**项目**: Nomos 可搜索加密方案
**论文来源**: 算法 3 (bf.tex:215-262)

---

## 一、核心问题

### 1.1 简化版本的安全缺陷

**问题**: 原始实现使用 `genTokenSimplified()`，Gatekeeper 直接计算令牌
```cpp
SearchToken genTokenSimplified(const std::vector<std::string>& query_keywords);
```

**安全问题**:
- ❌ Gatekeeper 可以看到查询关键词明文
- ❌ 不满足查询隐私 (Query Privacy)
- ❌ 不符合论文的 OPRF 安全模型

### 1.2 OPRF 协议目标

**目标**: 实现交互式盲化协议，使得：
- ✅ Client 不知道 Gatekeeper 的主密钥
- ✅ Gatekeeper 不知道 Client 的查询关键词
- ✅ 最终令牌功能等价于直接计算

---

## 二、数学原理

### 2.1 盲化与去盲化

**核心思想**: 使用随机盲化因子隐藏查询内容

**盲化过程**:
```
Client 计算: a = H(w)^r  (r 是随机盲化因子)
Gatekeeper 计算: a' = a^K = (H(w)^r)^K = H(w)^{r·K}
Client 去盲化: result = (a')^{r^{-1}} = H(w)^{r·K·r^{-1}} = H(w)^K
```

**关键性质**:
- Gatekeeper 只看到 `H(w)^r`，无法恢复 `w` (基于离散对数困难)
- Client 使用 `r^{-1}` 消除盲化因子
- 最终结果 `H(w)^K` 与直接计算相同

### 2.2 椭圆曲线群运算

**群**: 素阶 p 的椭圆曲线群 G
**生成元**: g
**运算**: 点乘 (scalar multiplication)

**关键操作**:
```cpp
ep_mul(result, point, scalar);  // result = point^scalar
bn_mod_inv(inv, x, ord);        // inv = x^{-1} mod ord
```

**安全假设**:
- 离散对数困难 (DL): 给定 g^x，计算 x 困难
- 计算 Diffie-Hellman (CDH): 给定 g^a, g^b，计算 g^{ab} 困难

---

## 三、协议设计

### 3.1 数据结构

**BlindedRequest** (Client → Gatekeeper):
```cpp
struct BlindedRequest {
    std::vector<std::string> a;     // a_j = H(w_j)^{r_j}, j=1..n
    std::vector<std::string> b;     // b_j = H(w_1||j||0)^{s_j}, j=1..m
    std::vector<std::string> c;     // c_j = H(w_1||j||1)^{s_j}, j=1..m
    std::vector<int> av;            // Access vector (I(w_1), ..., I(w_n))
};
```

**BlindedResponse** (Gatekeeper → Client):
```cpp
struct BlindedResponse {
    std::string strap_prime;                        // strap' = a_1^{K_S}
    std::vector<std::string> bstag_prime;           // bstag'_j = b_j^{K_T^{I_1} · gamma_j}
    std::vector<std::string> delta_prime;           // delta'_j = c_j^{K_T^{I_1}}
    std::vector<std::vector<std::string>> bxtrap_prime;  // bxtrap'_j[t]
    std::vector<uint8_t> env;                       // AE.Enc_{K_M}(rho, gamma)
};
```

**SearchToken** (最终令牌):
```cpp
struct SearchToken {
    ep_t strap;                                     // H(w1)^{K_S}
    std::vector<std::string> bstag;                 // bstag_j (unblinded)
    std::vector<std::string> delta;                 // delta_j (unblinded)
    std::vector<std::vector<std::string>> bxtrap;   // bxtrap_j[t] (unblinded)
    std::vector<uint8_t> env;                       // Encrypted (rho, gamma)
};
```

### 3.2 协议流程

#### Phase 1: Client 生成盲化请求

**算法 3, 行 1-6**

```cpp
BlindedRequest ClientCorrect::genTokenPhase1(
    const std::vector<std::string>& query_keywords,
    const std::unordered_map<std::string, int>& updateCnt)
```

**步骤**:
1. 获取参数: n = 关键词数, m = 主关键词更新次数
2. 采样盲化因子:
   ```cpp
   r_1, ..., r_n ← Zp*  // 关键词盲化因子
   s_1, ..., s_m ← Zp*  // stag 盲化因子
   ```
3. 计算盲化值:
   ```cpp
   a_j = H(w_j)^{r_j}, j=1..n
   b_j = H(w_1||j||0)^{s_j}, j=1..m
   c_j = H(w_1||j||1)^{s_j}, j=1..m
   ```
4. 计算访问向量:
   ```cpp
   av = (I(w_1), ..., I(w_n))  // I(w) = hash(w) mod d
   ```
5. 存储盲化因子 `r, s` 供 Phase 2 使用

**关键点**:
- 盲化因子必须随机采样 (安全性)
- 盲化因子必须保存 (去盲化需要)
- 椭圆曲线点序列化为字符串 (存储)

#### Phase 2: Gatekeeper 处理盲化请求

**算法 3, 行 7-14**

```cpp
BlindedResponse GatekeeperCorrect::genTokenGatekeeper(
    const BlindedRequest& request)
```

**步骤**:
1. 检查访问控制: `av ∈ P` (当前简化为总是允许)
2. 采样随机化参数:
   ```cpp
   rho_1, ..., rho_n ← Zp*  // 用于 xtoken 去盲化
   gamma_1, ..., gamma_m ← Zp*  // 用于 stag 去盲化
   ```
3. 计算盲化令牌:
   ```cpp
   strap' = (a_1)^{K_S}
   bstag'_j = (b_j)^{K_T^{I_1} · gamma_j}, j=1..m
   delta'_j = (c_j)^{K_T^{I_1}}, j=1..m
   bxtrap'_j = (a_j)^{K_X^{I_j} · rho_j}, j=2..n
   ```
4. 采样 RBF 随机索引:
   ```cpp
   beta_1, ..., beta_k ← [ℓ]  // k=2, ℓ=3
   ```
5. 计算采样后的 bxtrap:
   ```cpp
   overline{bxtrap}'_j[t] = (bxtrap'_j)^{beta_t}, t=1..k
   ```
6. 加密 env:
   ```cpp
   env = AE.Enc_{K_M}(rho_1..n, gamma_1..m)
   ```

**关键点**:
- Gatekeeper 使用主密钥 `K_S, K_T, K_X`
- Gatekeeper 不知道查询关键词 (输入已盲化)
- `rho, gamma` 加密在 env 中供 Server 使用

#### Phase 3: Client 去盲化

**算法 3, 行 15-19**

```cpp
SearchToken ClientCorrect::genTokenPhase2(
    const BlindedResponse& response)
```

**步骤**:
1. 计算 strap:
   ```cpp
   strap = (strap')^{r_1^{-1}}
   ```
2. 计算 bstag:
   ```cpp
   bstag_j = (bstag'_j)^{s_j^{-1}}, j=1..m
   ```
3. 计算 delta:
   ```cpp
   delta_j = (delta'_j)^{s_j^{-1}}, j=1..m
   ```
4. 计算 bxtrap:
   ```cpp
   bxtrap_j[t] = (bxtrap'_j[t])^{r_j^{-1}}, j=2..n, t=1..k
   ```
5. 复制 env
6. 清理盲化因子 `r, s`

**关键点**:
- 使用模逆 `r^{-1}, s^{-1}` 消除盲化
- 去盲化后令牌与直接计算等价
- 盲化因子使用后立即清理 (安全性)

---

## 四、实现细节

### 4.1 椭圆曲线点序列化

**问题**: RELIC 的 `ep_t` 是数组类型，不能直接存储在 `std::vector`

**解决方案**:
```cpp
// 序列化: ep_t → std::string
std::string serializePoint(const ep_t point) {
  uint8_t bytes[256];
  int len = ep_size_bin(point, 1);
  ep_write_bin(bytes, len, point, 1);
  return std::string(reinterpret_cast<char*>(bytes), len);
}

// 反序列化: std::string → ep_t
void deserializePoint(ep_t point, const std::string& str) {
  ep_read_bin(point, reinterpret_cast<const uint8_t*>(str.data()),
              str.length());
}
```

### 4.2 模逆计算

**问题**: 需要计算 `r^{-1} mod ord`

**解决方案**:
```cpp
bn_t ord, r, r_inv;
bn_new(ord);
bn_new(r);
bn_new(r_inv);

ep_curve_get_ord(ord);  // 获取群阶
bn_rand_mod(r, ord);    // 采样 r
bn_mod_inv(r_inv, r, ord);  // 计算 r^{-1}

// 验证: r * r_inv ≡ 1 (mod ord)
```

### 4.3 内存管理

**盲化因子存储**:
```cpp
class ClientCorrect {
private:
    std::vector<bn_t> m_r;  // r_1, ..., r_n
    std::vector<bn_t> m_s;  // s_1, ..., s_m

    void freeBlindingFactors() {
        for (auto& r : m_r) {
            if (r != nullptr) bn_free(r);
        }
        for (auto& s : m_s) {
            if (s != nullptr) bn_free(s);
        }
        m_r.clear();
        m_s.clear();
    }
};
```

**RAII 原则**:
- `bn_new()` 后必须 `bn_free()`
- `ep_new()` 后必须 `ep_free()`
- 使用 `new[]` 分配的数组必须 `delete[]`

### 4.4 env 加密

**当前实现** (简化):
```cpp
// XOR 加密
response.env.resize(plaintext.size());
for (size_t i = 0; i < plaintext.size(); ++i) {
    response.env[i] = plaintext[i] ^ m_Km[i % m_Km.size()];
}
```

**建议改进** (生产环境):
```cpp
// AES-GCM 加密
#include <openssl/evp.h>

std::vector<uint8_t> aes_gcm_encrypt(
    const std::vector<uint8_t>& key,
    const std::vector<uint8_t>& plaintext) {
    // 使用 OpenSSL EVP API 实现 AES-GCM
    // 返回 ciphertext || tag
}
```

---

## 五、正确性证明

### 5.1 定理: 去盲化等价性

**定理**: 去盲化后的令牌等价于直接计算的令牌

**证明** (以 strap 为例):

1. **Client Phase 1**:
   ```
   a_1 = H(w_1)^{r_1}
   ```

2. **Gatekeeper Phase 2**:
   ```
   strap' = (a_1)^{K_S}
          = (H(w_1)^{r_1})^{K_S}
          = H(w_1)^{r_1 · K_S}
   ```

3. **Client Phase 3**:
   ```
   strap = (strap')^{r_1^{-1}}
         = (H(w_1)^{r_1 · K_S})^{r_1^{-1}}
         = H(w_1)^{r_1 · K_S · r_1^{-1}}
         = H(w_1)^{K_S}  ✓
   ```

4. **直接计算**:
   ```
   strap_direct = H(w_1)^{K_S}
   ```

**结论**: `strap = strap_direct` ✓

**其他令牌的证明类似**:
- `bstag_j`: 盲化因子 `s_j` 被 `s_j^{-1}` 消除
- `delta_j`: 盲化因子 `s_j` 被 `s_j^{-1}` 消除
- `bxtrap_j`: 盲化因子 `r_j` 被 `r_j^{-1}` 消除

### 5.2 测试验证

**测试用例**: `OPRFTest.UnblindingCorrectness`

```cpp
// OPRF 协议
BlindedRequest request = client.genTokenPhase1(query, updateCnt);
BlindedResponse response = gatekeeper.genTokenGatekeeper(request);
SearchToken token_oprf = client.genTokenPhase2(response);

// 简化协议 (直接计算)
SearchToken token_simple = gatekeeper.genTokenSimplified(query);

// 验证等价性
EXPECT_EQ(serialize(token_oprf.strap), serialize(token_simple.strap));
EXPECT_EQ(token_oprf.bstag, token_simple.bstag);
EXPECT_EQ(token_oprf.delta, token_simple.delta);
```

**结果**: ✅ 所有测试通过

---

## 六、安全性分析

### 6.1 查询隐私 (Query Privacy)

**威胁模型**: 诚实但好奇的 Gatekeeper

**攻击目标**: 从盲化请求恢复查询关键词

**保护机制**:
- Client 发送 `a_j = H(w_j)^{r_j}`
- Gatekeeper 需要从 `a_j` 恢复 `w_j`
- 等价于求解离散对数: 给定 `g^x`，求 `x`

**安全性依赖**:
- **离散对数困难假设 (DL)**: 在椭圆曲线群上求解离散对数是困难的
- **随机性**: 每次查询使用新的随机 `r_j`，不同查询不可链接

**攻击复杂度**: O(√p) (Baby-step Giant-step) 或 O(2^{λ/2}) (Pollard's rho)
- 对于 256-bit 曲线，约 2^128 次运算 (不可行)

### 6.2 令牌不可伪造性 (Token Unforgeability)

**威胁模型**: 恶意 Client 试图伪造令牌

**攻击目标**: 在不与 Gatekeeper 交互的情况下生成有效令牌

**保护机制**:
- 令牌包含 `env = AE.Enc_{K_M}(rho, gamma)`
- `K_M` 由 Gatekeeper 和 Server 共享
- Client 不知道 `K_M`
- Server 在搜索前验证 `env` 的完整性

**安全性依赖**:
- **认证加密 (AE)**: INT-CTXT 完整性保证
- **密钥保密**: Client 无法获得 `K_M`

**当前实现**: XOR 加密 (简化)
- ⚠️ 不满足 INT-CTXT
- 🔧 建议升级为 AES-GCM

### 6.3 前向隐私 (Forward Privacy)

**定义**: 更新操作不泄露被更新关键词的身份

**实现**:
- Update 协议不依赖 OPRF
- 更新消息 `(addr, val, alpha, xtags)` 不包含关键词明文
- `addr = H(w||cnt||0)^{K_T^{I(w)}}` 是伪随机的

**结论**: ✅ 满足前向隐私

### 6.4 后向隐私 (Backward Privacy)

**定义**: 搜索泄露不包含已删除条目的历史信息

**实现**:
- 搜索返回 `(j, sval_j, cnt_j)`
- Client 解密后根据 `op` 字段过滤删除操作
- 泄露更新时间线但不泄露删除配对

**结论**: ✅ 满足 Type-II 后向隐私

---

## 七、性能分析

### 7.1 计算开销

| 操作 | 简化版本 | OPRF 版本 | 增加 |
|------|---------|----------|------|
| Client Phase 1 | - | n + 2m 次点乘 | +100% |
| Gatekeeper | n + 2m 次点乘 | 1 + 2m + (n-1) 次点乘 | +0% |
| Client Phase 3 | - | 1 + 2m + k(n-1) 次模逆 + 点乘 | +100% |
| **总计** | n + 2m | 2n + 4m + k(n-1) | ~2-3x |

**参数**: n=2 (关键词数), m=10 (更新次数), k=2 (采样数)

**结论**: OPRF 版本增加约 2-3 倍计算开销

### 7.2 通信开销

| 阶段 | 简化版本 | OPRF 版本 | 增加 |
|------|---------|----------|------|
| 请求 | - | n + 2m 个点 (~32 bytes/点) | +100% |
| 响应 | n + 2m 个点 + env | 1 + 2m + k(n-1) 个点 + env | +0% |
| **总计** | ~1 KB | ~2 KB | ~2x |

**结论**: OPRF 版本增加 1 轮通信，通信量约 2 倍

### 7.3 性能优化方向

1. **批量点乘**: 使用 RELIC 的批量操作
   ```cpp
   ep_mul_sim_lot(result, points, scalars, n);
   ```

2. **预计算**: 缓存常用的哈希值
   ```cpp
   std::unordered_map<std::string, ep_t> hash_cache;
   ```

3. **并行化**: Phase 1 和 Phase 3 的循环可并行
   ```cpp
   #pragma omp parallel for
   for (int j = 0; j < n; ++j) {
       // 计算 a_j
   }
   ```

---

## 八、实现检查清单

### 8.1 数据结构

- [x] `BlindedRequest` 定义
- [x] `BlindedResponse` 定义
- [x] `SearchToken` 更新注释

### 8.2 Client 端

- [x] `genTokenPhase1()` 实现
  - [x] 采样盲化因子 `r, s`
  - [x] 计算盲化值 `a, b, c`
  - [x] 计算访问向量 `av`
  - [x] 存储盲化因子
- [x] `genTokenPhase2()` 实现
  - [x] 计算模逆 `r^{-1}, s^{-1}`
  - [x] 去盲化 `strap, bstag, delta, bxtrap`
  - [x] 清理盲化因子
- [x] `freeBlindingFactors()` 实现
- [x] 析构函数更新

### 8.3 Gatekeeper 端

- [x] `genTokenGatekeeper()` 实现
  - [x] 访问控制检查 (简化)
  - [x] 采样随机化参数 `rho, gamma`
  - [x] 计算盲化令牌
  - [x] 采样 RBF 索引 `beta`
  - [x] 加密 env

### 8.4 测试

- [x] `OPRFTest.FullOPRFProtocol` - 完整协议
- [x] `OPRFTest.BlindingFactorsRandomness` - 随机性
- [x] `OPRFTest.UnblindingCorrectness` - 正确性
- [x] `OPRFTest.EnvEncryption` - env 加密

### 8.5 文档

- [x] 实现文档 (`OPRF-Implementation.md`)
- [x] 实现总结 (`OPRF实现总结.md`)
- [x] 实现思路 (本文档)

---

## 九、常见问题

### Q1: 为什么需要盲化因子？

**A**: 盲化因子 `r` 隐藏查询关键词，使 Gatekeeper 无法从 `H(w)^r` 恢复 `w`。

### Q2: 为什么去盲化后令牌与直接计算等价？

**A**: 因为 `(H(w)^r)^K)^{r^{-1}} = H(w)^{r·K·r^{-1}} = H(w)^K`，盲化因子被消除。

### Q3: 为什么每次查询使用新的盲化因子？

**A**: 防止查询链接攻击。如果重用 `r`，Gatekeeper 可以识别相同查询。

### Q4: env 为什么需要加密？

**A**: env 包含 `rho, gamma` 参数，Server 需要用它们去盲化 xtoken。如果不加密，Client 可以伪造令牌。

### Q5: 为什么使用椭圆曲线而不是 RSA？

**A**: 椭圆曲线提供更短的密钥长度和更快的运算速度。256-bit 椭圆曲线 ≈ 3072-bit RSA。

### Q6: 如何验证实现正确性？

**A**: 运行 `OPRFTest.UnblindingCorrectness` 测试，验证 OPRF 令牌 = 简化令牌。

### Q7: 性能开销可接受吗？

**A**: 是的。OPRF 增加约 2-3 倍计算开销和 1 轮通信，但提供了查询隐私保护，这是论文安全模型的核心要求。

### Q8: 可以跳过 OPRF 吗？

**A**: 不建议。跳过 OPRF 意味着不满足论文的安全模型，只能用于测试，不能用于生产环境。

---

## 十、后续工作

### 10.1 高优先级

1. **升级 env 加密**
   - 当前: XOR
   - 目标: AES-GCM
   - 影响: 令牌不可伪造性

2. **实现访问控制**
   - 当前: 总是允许
   - 目标: 检查 `av ∈ P`
   - 影响: 细粒度权限控制

### 10.2 中优先级

3. **参数化配置**
   - 当前: 硬编码 `k=2, ℓ=3, d=10`
   - 目标: 配置文件或构造函数参数
   - 影响: 灵活性

4. **错误处理**
   - 当前: 返回空结构
   - 目标: `std::optional` 或异常
   - 影响: 调试体验

### 10.3 低优先级

5. **性能优化**
   - 批量点乘
   - 预计算哈希
   - 并行化循环

6. **安全增强**
   - 常数时间操作
   - 内存清零
   - 硬件 RNG

---

## 十一、参考资料

### 11.1 论文

- Bag et al. 2024: "Tokenised Multi-client Provisioning for Dynamic Searchable Encryption"
- 算法 3: OPRF 盲化令牌生成协议 (bf.tex:215-262)

### 11.2 密码学原语

- RELIC 库: https://github.com/relic-toolkit/relic
- 椭圆曲线密码学: Guide to Elliptic Curve Cryptography (Hankerson et al.)
- OPRF: Freedman et al. 2005

### 11.3 代码文件

- `include/nomos/types_correct.hpp`: 数据结构
- `include/nomos/GatekeeperCorrect.hpp`: Gatekeeper 接口
- `include/nomos/ClientCorrect.hpp`: Client 接口
- `src/nomos/GatekeeperCorrect.cpp`: Gatekeeper 实现
- `src/nomos/ClientCorrect.cpp`: Client 实现
- `tests/oprf_test.cpp`: 测试套件

---

**文档版本**: 1.0
**最后更新**: 2026-03-07
**作者**: Claude Opus 4.6
**状态**: 完成并验证
