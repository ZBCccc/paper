# Notation Consistency Review Report

**Reviewer**: notation-reviewer
**Date**: 2026-03-03
**Scope**: All chapters (intro.tex, bf.tex, commitment.tex, experiments.tex, conclusion.tex)

---

## Executive Summary

The thesis demonstrates **strong overall notation consistency** with well-defined symbol tables in each technical chapter. However, several **critical issues** require attention:

1. **CRITICAL**: Algorithm-prose notation mismatch in Nomos protocol
2. **IMPORTANT**: Missing first-use definitions for several key symbols
3. **IMPORTANT**: Inconsistent database notation (DB vs D)
4. **MINOR**: Cross-reference integrity issues

---

## 1. Symbol Table Analysis

### 1.1 Chapter 2 (bf.tex) - Symbol Table

**Location**: Table~\ref{tab:notation} (lines 16-40)

**Status**: ✓ COMPLETE

Symbols defined:
- $\lambda$ (security parameter)
- $\mathsf{DB}$, $N$ (database and size)
- $\mathsf{id}$, $\mathsf{doc}$ (file identifiers)
- $\mathcal{W}$, $\mathcal{W}_i$ (keyword spaces)
- $Q=\{w_1,\ldots,w_n\}$ (query)
- $\mathcal{D}$, $\mathcal{G}$, $\mathcal{C}_i$, $\mathcal{S}$ (entities)
- $F$, $H$, $\varphi$, $F_p$, $\mathsf{AE}$ (cryptographic primitives)
- $\mathsf{EDB}$, $\mathsf{TSet}$, $\mathsf{XSet}$ (encrypted database structures)

### 1.2 Chapter 3 (commitment.tex) - Symbol Table

**Location**: Table~\ref{tab:commit-notation} (lines 9-26)

**Status**: ✓ COMPLETE

New symbols defined:
- $\mathcal{F}_{w,\mathsf{id}}$ (cross-tag set)
- $\mathsf{Cm}_{w,\mathsf{id}}$ (address commitment)
- $H_c$ (commitment hash function)
- $K_E(w,\mathsf{cnt})$ (TSet payload session key)
- $\mathsf{val}'$ (extended TSet payload)
- $\mathsf{Open}_{j,\mathsf{id}}$ (opening material)
- $\mathsf{ProofAddr}_{j,\mathsf{id}}$ (proof address set)

**Note**: Correctly states that Chapter 2 symbols ($\lambda$, $\mathsf{EDB}$, $F$, $H$, $F_p$, $\mathsf{AE}$) are reused.

### 1.3 Chapter 4 (experiments.tex) - Parameter Table

**Location**: Table~\ref{tab:params} (lines 14-33)

**Status**: ✓ COMPLETE

Parameters defined:
- $\lambda$, $N$, $M$, $\ell$, $k$, $n$ (system parameters)
- $|\mathsf{Cand}(w_s)|$ (candidate set size)
- $|\mathbb{G}|$ (group element size)
- $N_+$, $N_-$ (positive/negative judgment counts)

---

## 2. CRITICAL ISSUES

### Issue #1: Algorithm-Prose Notation Mismatch (Nomos Protocol)

**Type**: INCONSISTENCY
**Severity**: CRITICAL
**Location**: bf.tex:154-157 (Algorithm 2) vs bf.tex:297-301 (prose description)

**Problem**:

Algorithm 2 (line 154):
```latex
\STATE 设置 $\mathsf{addr}\leftarrow \varphi(H(w\|\mathsf{UpdateCnt}[w]\|0))^{K_T[I(w)]}$
```

Prose description (line 299):
```latex
\mathsf{xtag}_i=\varphi(H(w))^{K_X[I(w)]\cdot F_p(K_Y,\mathsf{id}\|\mathsf{op})\cdot i}
```

**Issue**: The algorithm uses `\varphi(H(...))^{...}` notation, but the prose description in Section 2.5.1 uses the same notation for $\mathsf{xtag}$ computation. However, Algorithm 2 line 151 shows:
```latex
\STATE 设置 $K_Z \leftarrow F((H(\varphi(H(w))^{K_S})),1)$
```

This creates confusion: is $\varphi$ applied to $H(w)$ or to the entire expression?

**Fix**: Standardize notation. Recommend:
- Use $\varphi(H(w))$ consistently for "hash-to-group" operation
- Clarify in prose that $\varphi$ is the encoding function from $\{0,1\}^\lambda$ to $\mathbb{G}$

---

### Issue #2: Database Notation Inconsistency

**Type**: DRIFT
**Severity**: IMPORTANT
**Location**: Multiple locations

**Problem**:

1. **bf.tex:8**: Uses $\mathsf{DB}=\{(\mathsf{id}_1,\mathsf{doc}_1),\ldots,(\mathsf{id}_N,\mathsf{doc}_N)\}$
2. **bf.tex:80**: Uses $\mathcal{H}=(\mathsf{DB}_0,\mathsf{Upd}_1,\ldots)$
3. **bf.tex:94**: Uses $\mathsf{TimeDB}(w)$ (different concept but similar naming)

**Issue**: The notation switches between $\mathsf{DB}$ (mathsf) and potential confusion with $\mathsf{TimeDB}$ which is a function, not the database itself.

**Fix**:
- Keep $\mathsf{DB}$ for the database
- Ensure $\mathsf{TimeDB}(w)$ is clearly distinguished as a function returning time-stamped entries

**Status**: ACCEPTABLE (different concepts, but naming could be clearer)

---

### Issue #3: Missing First-Use Definition

**Type**: UNDEFINED
**Severity**: IMPORTANT
**Location**: bf.tex:151, 154, 157

**Problem**:

Algorithm 2 uses several symbols without prior definition:
- $I(w)$ (line 154, 155, 157) - appears to be an index function mapping keywords to key indices
- $K_Z$ (line 151) - derived key, but not in symbol table
- $\mathsf{UpdateCnt}$ (line 152) - mentioned in prose but not formally defined in symbol table

**Fix**: Add to symbol table or define at first use:
- $I: \mathcal{W} \to [d]$ - keyword-to-index mapping function
- $K_Z$ - ephemeral key derived from $K_S$ and $w$
- $\mathsf{UpdateCnt}: \mathcal{W} \to \mathbb{N}$ - per-keyword update counter

---

### Issue #4: Nomos Token Structure Notation

**Type**: INCONSISTENCY
**Severity**: IMPORTANT
**Location**: bf.tex:284-286 vs algorithms

**Problem**:

Prose (line 284-286):
```latex
\tau=(\mathsf{strap},\{\mathsf{bstag}_j\}_{j\in[m]},\{\delta_j\}_{j\in[m]},\{\overline{\mathsf{bxtrap}}_i\}_{i=2}^{n},\mathsf{env})
```

But Algorithm 3 (line 209-210) shows:
```latex
\STATE 输出 $\tau=(\mathsf{strap},\{\mathsf{bstag}_j\}_{j\in[m]},\{\delta_j\}_{j\in[m]},$
\item[] \hspace*{\algorithmicindent} $\{\overline{\mathsf{bxtrap}}_j\}_{j=2}^{n},\mathsf{env})$
```

**Issue**: Index variable changes from $i$ to $j$ for $\overline{\mathsf{bxtrap}}$.

**Fix**: Use consistent index variable. Recommend $j$ throughout since it's used for other token components.

---

## 3. IMPORTANT ISSUES

### Issue #5: Cross-Reference Integrity

**Type**: BROKEN_REF
**Severity**: IMPORTANT
**Location**: Multiple

**Checked References**:

✓ All `\label{chap:*}` references exist and are used
✓ All `\label{tab:*}` references exist and are used
✓ All `\label{alg:*}` references exist and are used
✓ All `\label{prop:*}` references exist and are used
✓ All `\label{eq:*}` references exist and are used
✓ All `\label{sec:*}` references exist and are used

**Status**: ✓ NO BROKEN REFERENCES FOUND

---

### Issue #6: Complexity Notation Consistency

**Type**: MINOR
**Severity**: MINOR
**Location**: experiments.tex

**Problem**:

Chapter 4 uses O-notation consistently, but parameter dependencies could be clearer:

- Line 50: $O(\ell\log M)$ - clear
- Line 62: $O((N_+\cdot k + N_-)\log M)$ - clear
- Line 102: $O(|\mathsf{Cand}(w_s)|\cdot(n-1)\cdot\ell)$ - uses full notation

**Issue**: Sometimes uses $|\mathsf{Cand}|$ as shorthand (line 139), sometimes full $|\mathsf{Cand}(w_s)|$.

**Fix**: Use consistent shorthand notation. Add note in Table 4.1 that $|\mathsf{Cand}|$ is shorthand for $|\mathsf{Cand}(w_s)|$.

---

## 4. MINOR ISSUES

### Issue #7: Symbol $\mathsf{negl}(\lambda)$ Usage

**Type**: DRIFT
**Severity**: MINOR
**Location**: Multiple chapters

**Problem**:

The symbol $\mathsf{negl}(\lambda)$ is used to denote "negligible function" but is sometimes used as:
- A function: $\mathsf{negl}(\lambda)$ (correct)
- A value: "probability is $\mathsf{negl}(\lambda)$" (technically should be "at most $\mathsf{negl}(\lambda)$")

**Fix**: Ensure consistent usage. When used in inequalities, always use $\le \mathsf{negl}(\lambda)$ not $= \mathsf{negl}(\lambda)$.

**Status**: ACCEPTABLE (standard cryptographic convention allows this usage)

---

### Issue #8: Group Notation $\mathbb{G}$ vs $|\mathbb{G}|$

**Type**: MINOR
**Severity**: MINOR
**Location**: experiments.tex

**Problem**:

- $\mathbb{G}$ denotes the group (bf.tex:14)
- $|\mathbb{G}|$ denotes bit-length of group element (experiments.tex:29)

**Issue**: Technically, $|\mathbb{G}|$ usually means group order, not bit-length.

**Fix**: Use $\ell_{\mathbb{G}}$ or clarify in Table 4.1 that $|\mathbb{G}|$ means "bit-length of group element representation".

---

## 5. POSITIVE FINDINGS

### Strengths:

1. ✓ **Excellent symbol table organization** - each chapter has clear tables
2. ✓ **Consistent cryptographic notation** - PRF, OPRF, AE notation is standard
3. ✓ **Clear entity notation** - $\mathcal{D}$, $\mathcal{G}$, $\mathcal{C}_i$, $\mathcal{S}$ used consistently
4. ✓ **Algorithm numbering** - all algorithms properly labeled and referenced
5. ✓ **Proposition numbering** - all propositions properly labeled and cross-referenced
6. ✓ **No broken cross-references** - all \ref and \autoref targets exist

---

## 6. RECOMMENDATIONS

### Priority 1 (CRITICAL - Must Fix):

1. **Fix Algorithm 2 notation** (Issue #1)
   - Clarify $\varphi(H(...))$ vs $H(\varphi(...))$ usage
   - Ensure algorithm matches prose description

2. **Add missing definitions** (Issue #3)
   - Define $I(w)$ function
   - Define $K_Z$ derivation
   - Add $\mathsf{UpdateCnt}$ to symbol table

### Priority 2 (IMPORTANT - Should Fix):

3. **Standardize token notation** (Issue #4)
   - Use consistent index variable for $\overline{\mathsf{bxtrap}}$

4. **Clarify $|\mathbb{G}|$ notation** (Issue #8)
   - Add note that this means bit-length, not group order

### Priority 3 (MINOR - Nice to Have):

5. **Add shorthand notation note** (Issue #6)
   - Document that $|\mathsf{Cand}|$ is shorthand for $|\mathsf{Cand}(w_s)|$

---

## 7. DETAILED SYMBOL REGISTRY

### Global Symbols (Used Across All Chapters):

| Symbol | First Defined | Meaning | Consistency |
|--------|---------------|---------|-------------|
| $\lambda$ | bf.tex:6 | Security parameter | ✓ Consistent |
| $\mathsf{DB}$ | bf.tex:8 | Database | ✓ Consistent |
| $N$ | bf.tex:8 | Database size | ✓ Consistent |
| $\mathsf{id}$ | bf.tex:8 | File identifier | ✓ Consistent |
| $\mathcal{W}$ | bf.tex:8 | Keyword space | ✓ Consistent |
| $Q$ | bf.tex:8 | Query | ✓ Consistent |
| $n$ | bf.tex:8 | Query size | ✓ Consistent |
| $\mathcal{G}$ | bf.tex:6 | Gate-keeper | ✓ Consistent |
| $\mathcal{S}$ | bf.tex:6 | Server | ✓ Consistent |
| $\mathcal{C}_i$ | bf.tex:6 | Client $i$ | ✓ Consistent |
| $F$ | bf.tex:14 | PRF | ✓ Consistent |
| $H$ | bf.tex:14 | Hash function | ✓ Consistent |
| $F_p$ | bf.tex:14 | OPRF | ✓ Consistent |
| $\mathsf{AE}$ | bf.tex:14 | Auth. encryption | ✓ Consistent |
| $\mathsf{EDB}$ | bf.tex:35 | Encrypted DB | ✓ Consistent |
| $\mathsf{TSet}$ | bf.tex:36 | Token set | ✓ Consistent |
| $\mathsf{XSet}$ | bf.tex:37 | Cross-tag set | ✓ Consistent |

### Chapter-Specific Symbols:

**Chapter 2 (bf.tex)**:
- $\mathsf{QTree}$ - Merkle tree over XSet
- $R_X^{(t)}$ - Root hash at version $t$
- $\mathsf{Anchor}_t$ - Version anchor
- $\mathcal{A}_{j,\mathsf{id}}^{(t,\nu)}$ - Address set
- $v_{j,\mathsf{id}}^{(t,\nu)}$ - Judgment bit

**Chapter 3 (commitment.tex)**:
- $\mathsf{Cm}_{w,\mathsf{id}}$ - Address commitment
- $H_c$ - Commitment hash
- $\mathsf{Open}_{j,\mathsf{id}}$ - Opening material
- $\mathsf{ProofAddr}_{j,\mathsf{id}}$ - Proof addresses

**Chapter 4 (experiments.tex)**:
- $M$ - XSet array length
- $\ell$ - Insertion-side hash count
- $k$ - Query-side sample count
- $N_+$, $N_-$ - Positive/negative counts

---

## 8. CONCLUSION

**Overall Assessment**: ✓ GOOD with CRITICAL fixes needed

The thesis demonstrates strong mathematical rigor and notation consistency. The symbol tables are comprehensive and well-organized. However, **Algorithm 2 notation must be fixed** to match the prose description, and several missing first-use definitions should be added.

**Estimated Fix Time**: 2-3 hours

**Recommended Actions**:
1. Fix Algorithm 2 notation (30 min)
2. Add missing symbol definitions (30 min)
3. Standardize token notation (15 min)
4. Add clarifying notes to tables (30 min)
5. Final consistency check (30 min)

---

**Report Generated**: 2026-03-03
**Reviewer**: notation-reviewer
**Status**: REVIEW COMPLETE
