# 实验数据实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal**: 为硕士论文实现三个方案的完整实验数据：Nomos（基线）、MC-ODXT（对比方案）、VQNomos（本文方案）

**Architecture**: 基于现有 Nomos 代码库，扩展 benchmark 框架，实现三个方案的性能评估，生成论文第四章所需的实验数据

**Tech Stack**: C++11, RELIC (椭圆曲线), OpenSSL (哈希), GMP (大整数), GoogleTest (测试)

---

## Task 1: 完善 Nomos 基线方案的 Benchmark 框架

**Files:**
- Modify: `Nomos/include/benchmark/NomosBenchmark.hpp`
- Modify: `Nomos/src/benchmark/NomosBenchmark.cpp`
- Modify: `Nomos/include/benchmark/BenchmarkExperiment.hpp`
- Modify: `Nomos/src/benchmark/BenchmarkExperiment.cpp`

**Step 1: 设计 Benchmark 数据结构**

在 `NomosBenchmark.hpp` 中添加：

```cpp
struct BenchmarkResult {
    // 时间指标
    double setup_time_ms;
    double update_time_ms;
    double search_time_ms;

    // 存储指标
    size_t tset_size_bytes;
    size_t xset_size_bytes;
    size_t total_storage_bytes;

    // 通信指标
    size_t token_size_bytes;
    size_t response_size_bytes;

    // 参数
    int num_documents;
    int num_keywords;
    int query_keywords;
};

class NomosBenchmark {
public:
    BenchmarkResult runBenchmark(int N, int num_keywords, int query_size);
    void exportToCSV(const std::string& filename);
private:
    std::vector<BenchmarkResult> results_;
};
```

**Step 2: 实现 Benchmark 核心逻辑**

在 `NomosBenchmark.cpp` 中实现：

```cpp
BenchmarkResult NomosBenchmark::runBenchmark(int N, int num_keywords, int query_size) {
    BenchmarkResult result;
    result.num_documents = N;
    result.num_keywords = num_keywords;
    result.query_keywords = query_size;

    // Setup phase
    auto start = std::chrono::high_resolution_clock::now();
    GatekeeperCorrect gatekeeper;
    gatekeeper.setup(10);
    auto end = std::chrono::high_resolution_clock::now();
    result.setup_time_ms = std::chrono::duration<double, std::milli>(end - start).count();

    // Update phase (measure average)
    // ... implementation

    // Search phase
    // ... implementation

    return result;
}
```

**Step 3: 运行测试**

Run: `cd build && cmake .. && make && ./Nomos benchmark`
Expected: 输出 Benchmark 结果

**Step 4: Commit**

```bash
git add include/benchmark/* src/benchmark/*
git commit -m "feat: implement Nomos baseline benchmark framework"
```

---

## Task 2: 实现 MC-ODXT 方案的核心协议

**Files:**
- Create: `Nomos/include/mc-odxt/McOdxtTypes.hpp`
- Create: `Nomos/include/mc-odxt/McOdxtProtocol.hpp`
- Create: `Nomos/src/mc-odxt/McOdxtProtocol.cpp`

**Step 1: 定义 MC-ODXT 数据结构**

在 `McOdxtTypes.hpp` 中：

```cpp
struct McOdxtIndex {
    std::map<std::string, std::vector<std::string>> TSet;  // keyword -> encrypted tuples
    std::map<std::string, bool> XSet;  // xtag -> bit
};

struct McOdxtToken {
    std::string stag;
    std::vector<std::string> xtoken_list;
};
```

**Step 2: 实现 MC-ODXT Setup**

在 `McOdxtProtocol.cpp` 中：

```cpp
void McOdxtProtocol::setup() {
    // Generate keys
    // Initialize TSet and XSet
}
```

**Step 3: 实现 MC-ODXT Update**

```cpp
void McOdxtProtocol::update(const std::string& keyword, const std::string& id, bool op) {
    // Compute stag
    // Compute xtags
    // Update TSet and XSet
}
```

**Step 4: 实现 MC-ODXT Search**

```cpp
std::vector<std::string> McOdxtProtocol::search(const McOdxtToken& token) {
    // Retrieve from TSet
    // Filter with XSet
    // Return results
}
```

**Step 5: 运行测试**

Run: `./tests/nomos_test --gtest_filter=McOdxtTest.*`
Expected: PASS

**Step 6: Commit**

```bash
git add include/mc-odxt/* src/mc-odxt/*
git commit -m "feat: implement MC-ODXT core protocol"
```

---

## Task 3: 实现 VQNomos 方案的完整协议

**Files:**
- Modify: `Nomos/include/verifiable/QTree.hpp`
- Modify: `Nomos/src/verifiable/QTree.cpp`
- Modify: `Nomos/include/verifiable/AddressCommitment.hpp`
- Modify: `Nomos/src/verifiable/AddressCommitment.cpp`
- Create: `Nomos/include/verifiable/VQNomosScheme.hpp`
- Create: `Nomos/src/verifiable/VQNomosScheme.cpp`

**Step 1: 修复 QTree 路径验证**

在 `QTree.cpp` 中修正索引映射：

```cpp
bool QTree::verifyPath(const AuthPath& path, size_t address, bool bit_value) {
    std::string current_hash = hashLeaf(address, bit_value);
    size_t index = address;

    for (const auto& sibling : path.siblings) {
        if (index % 2 == 0) {
            current_hash = hashInternal(current_hash, sibling);
        } else {
            current_hash = hashInternal(sibling, current_hash);
        }
        index /= 2;
    }

    return current_hash == root_hash_;
}
```

**Step 2: 集成 QTree 与 AddressCommitment**

在 `VQNomosScheme.hpp` 中：

```cpp
class VQNomosScheme {
public:
    void setup();
    void update(const std::string& keyword, const std::string& id, bool op);
    VerifiableSearchResult search(const SearchToken& token);
    bool verify(const VerifiableSearchResult& result);

private:
    GatekeeperCorrect gatekeeper_;
    ServerCorrect server_;
    QTree qtree_;
    AddressCommitment commitment_;
};
```

**Step 3: 实现 VQNomos Update**

```cpp
void VQNomosScheme::update(const std::string& keyword, const std::string& id, bool op) {
    // 1. Nomos baseline update
    // 2. Update QTree
    // 3. Compute commitment
}
```

**Step 4: 实现 VQNomos Search with Proof**

```cpp
VerifiableSearchResult VQNomosScheme::search(const SearchToken& token) {
    // 1. Nomos baseline search
    // 2. Generate QTree proofs
    // 3. Generate opening materials
    return result;
}
```

**Step 5: 运行测试**

Run: `./tests/nomos_test --gtest_filter=VQNomosTest.*`
Expected: PASS

**Step 6: Commit**

```bash
git add include/verifiable/* src/verifiable/*
git commit -m "feat: implement VQNomos complete verifiable scheme"
```

---

## Task 4: 实现三方案对比 Benchmark

**Files:**
- Create: `Nomos/include/benchmark/ComparativeBenchmark.hpp`
- Create: `Nomos/src/benchmark/ComparativeBenchmark.cpp`

**Step 1: 设计对比实验框架**

```cpp
struct ComparisonResult {
    std::string scheme_name;
    BenchmarkResult nomos_result;
    BenchmarkResult mcodxt_result;
    BenchmarkResult vqnomos_result;
};

class ComparativeBenchmark {
public:
    ComparisonResult runComparison(int N, int num_keywords, int query_size);
    void exportToCSV(const std::string& filename);
};
```

**Step 2: 实现对比实验**

```cpp
ComparisonResult ComparativeBenchmark::runComparison(int N, int num_keywords, int query_size) {
    ComparisonResult result;

    // Run Nomos
    NomosBenchmark nomos_bench;
    result.nomos_result = nomos_bench.runBenchmark(N, num_keywords, query_size);

    // Run MC-ODXT
    McOdxtBenchmark mcodxt_bench;
    result.mcodxt_result = mcodxt_bench.runBenchmark(N, num_keywords, query_size);

    // Run VQNomos
    VQNomosBenchmark vqnomos_bench;
    result.vqnomos_result = vqnomos_bench.runBenchmark(N, num_keywords, query_size);

    return result;
}
```

**Step 3: 实现 CSV 导出**

```cpp
void ComparativeBenchmark::exportToCSV(const std::string& filename) {
    std::ofstream file(filename);
    file << "Scheme,N,Keywords,QuerySize,SetupTime,UpdateTime,SearchTime,Storage\n";
    // ... write data
}
```

**Step 4: 运行对比实验**

Run: `./Nomos comparative-benchmark --output results.csv`
Expected: 生成 results.csv

**Step 5: Commit**

```bash
git add include/benchmark/ComparativeBenchmark.* src/benchmark/ComparativeBenchmark.*
git commit -m "feat: implement comparative benchmark for three schemes"
```

---

## Task 5: 生成论文实验数据

**Files:**
- Create: `Nomos/scripts/generate_experiment_data.sh`
- Create: `Nomos/scripts/plot_results.py`

**Step 1: 编写实验脚本**

```bash
#!/bin/bash
# generate_experiment_data.sh

# Experiment 1: Scalability (varying N)
for N in 100 500 1000 5000 10000; do
    ./Nomos comparative-benchmark --N $N --keywords 100 --query-size 3 --output exp1_N${N}.csv
done

# Experiment 2: Query complexity (varying n)
for n in 1 2 3 4 5; do
    ./Nomos comparative-benchmark --N 1000 --keywords 100 --query-size $n --output exp2_n${n}.csv
done

# Experiment 3: Parameter sensitivity (varying ℓ and k)
for ell in 10 20 50; do
    for k in 5 10 20; do
        ./Nomos comparative-benchmark --N 1000 --ell $ell --k $k --output exp3_ell${ell}_k${k}.csv
    done
done
```

**Step 2: 编写绘图脚本**

```python
# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt

def plot_scalability():
    # Read CSV files
    # Plot N vs Time
    # Save to update-time.pdf, search-time.pdf
    pass

def plot_query_complexity():
    # Plot n vs Time
    pass

def plot_parameter_sensitivity():
    # Plot ℓ, k vs Time
    pass

if __name__ == "__main__":
    plot_scalability()
    plot_query_complexity()
    plot_parameter_sensitivity()
```

**Step 3: 运行实验**

Run: `bash scripts/generate_experiment_data.sh`
Expected: 生成多个 CSV 文件

**Step 4: 生成图表**

Run: `python scripts/plot_results.py`
Expected: 生成 PDF 图表文件

**Step 5: Commit**

```bash
git add scripts/* results/*.csv results/*.pdf
git commit -m "feat: generate experimental data for thesis chapter 4"
```

---

## Task 6: 验证实验数据与论文一致性

**Files:**
- Create: `Nomos/docs/experiment-validation.md`

**Step 1: 对比理论复杂度与实验结果**

检查：
- Update 时间是否符合 O(ℓ log M)
- Search 时间是否符合 O(|Cand| · (n-1) · (k log M + ℓ))
- 存储开销是否符合 O(N·ℓ + M·λ)

**Step 2: 编写验证报告**

```markdown
# 实验数据验证报告

## 1. Nomos 基线
- Update 时间: 实测 X ms, 理论 O(ℓ) ✓
- Search 时间: 实测 Y ms, 理论 O(|Cand|·k·(n-1)) ✓

## 2. VQNomos
- Update 时间: 实测 X ms, 理论 O(ℓ log M) ✓
- Search 时间: 实测 Y ms, 理论 O(|Cand|·(n-1)·(k log M + ℓ)) ✓

## 3. MC-ODXT
- Update 时间: 实测 X ms, 理论 O(1) ✓
- Search 时间: 实测 Y ms, 理论 O(N_+) ✓
```

**Step 3: Commit**

```bash
git add docs/experiment-validation.md
git commit -m "docs: validate experimental data against theoretical analysis"
```

---

## Execution Handoff

计划已完成并保存至 `docs/plans/2026-03-08-experimental-implementation.md`。

两种执行方式：

**1. Subagent-Driven (本会话)** - 我在本会话中为每个任务派发新的 subagent，任务间进行审查，快速迭代

**2. Parallel Session (独立会话)** - 在新会话中使用 executing-plans skill，批量执行并设置检查点

你希望使用哪种方式？
