# RAG Evaluation Results

## Summary

| Metric | Score |
|--------|-------|
| **Groundedness** | 100.0% |
| **Citation Accuracy** | 90.0% |
| **Partial Match (Gold)** | 83.3% |
| **Latency p50** | 2.172s |
| **Latency p95** | 2.882s |
| **Latency avg** | 2.298s |
| **Questions evaluated** | 30 |

## Per-Question Results

| ID | Category | Grounded | Citation | Partial Match | Latency | Sources |
|----|----------|----------|----------|---------------|---------|---------|
| Q01 | PTO | ✅ | ✅ | ✅ | 3.821s | performance-policy.md, pto-policy.md, expense-policy.md |
| Q02 | PTO | ✅ | ✅ | ✅ | 2.851s | pto-policy.md, training-policy.md, remote-work-policy.md |
| Q03 | PTO | ✅ | ✅ | ✅ | 2.312s | pto-policy.md, training-policy.md, performance-policy.md |
| Q04 | PTO | ✅ | ✅ | ✅ | 2.38s | pto-policy.md, training-policy.md, expense-policy.md, code-of-conduct.md |
| Q05 | PTO | ✅ | ✅ | ✅ | 2.134s | pto-policy.md, health-benefits-policy.md, code-of-conduct.md |
| Q06 | RemoteWork | ✅ | ✅ | ✅ | 2.056s | remote-work-policy.md, expense-policy.md, pto-policy.md, it-policy.md |
| Q07 | RemoteWork | ✅ | ✅ | ✅ | 2.302s | remote-work-policy.md, onboarding-policy.md, training-policy.md |
| Q08 | RemoteWork | ✅ | ✅ | ✅ | 2.128s | remote-work-policy.md, onboarding-policy.md, it-policy.md, health-benefits-policy.md, expense-policy.md |
| Q09 | RemoteWork | ✅ | ✅ | ✅ | 2.155s | remote-work-policy.md, expense-policy.md, training-policy.md, health-benefits-policy.md |
| Q10 | Expense | ✅ | ✅ | ✅ | 2.107s | expense-policy.md, onboarding-policy.md, it-policy.md |
| Q11 | Expense | ✅ | ✅ | ✅ | 2.282s | expense-policy.md, onboarding-policy.md, code-of-conduct.md |
| Q12 | Expense | ✅ | ✅ | ✅ | 2.139s | expense-policy.md, remote-work-policy.md, health-benefits-policy.md, code-of-conduct.md |
| Q13 | Expense | ✅ | ✅ | ✅ | 2.124s | expense-policy.md, code-of-conduct.md, pto-policy.md |
| Q14 | Security | ✅ | ✅ | ❌ | 2.141s | onboarding-policy.md, security-policy.md, remote-work-policy.md, pto-policy.md |
| Q15 | Security | ✅ | ✅ | ✅ | 2.2s | security-policy.md, it-policy.md, remote-work-policy.md |
| Q16 | Security | ✅ | ✅ | ✅ | 2.134s | security-policy.md, it-policy.md, code-of-conduct.md |
| Q17 | CodeOfConduct | ✅ | ❌ | ✅ | 2.175s | onboarding-policy.md, health-benefits-policy.md, performance-policy.md, training-policy.md |
| Q18 | Performance | ✅ | ✅ | ❌ | 2.29s | performance-policy.md, code-of-conduct.md, health-benefits-policy.md |
| Q19 | Performance | ✅ | ✅ | ✅ | 2.133s | performance-policy.md, training-policy.md, code-of-conduct.md |
| Q20 | Onboarding | ✅ | ❌ | ❌ | 2.085s | performance-policy.md, expense-policy.md, remote-work-policy.md, training-policy.md |
| Q21 | Onboarding | ✅ | ✅ | ✅ | 1.985s | onboarding-policy.md, security-policy.md, health-benefits-policy.md, it-policy.md, pto-policy.md |
| Q22 | Training | ✅ | ✅ | ❌ | 2.503s | onboarding-policy.md, training-policy.md, remote-work-policy.md |
| Q23 | Training | ✅ | ❌ | ❌ | 2.312s | performance-policy.md, health-benefits-policy.md, code-of-conduct.md, expense-policy.md, security-policy.md |
| Q24 | Benefits | ✅ | ✅ | ✅ | 2.359s | health-benefits-policy.md, code-of-conduct.md, onboarding-policy.md, pto-policy.md |
| Q25 | Benefits | ✅ | ✅ | ✅ | 2.347s | health-benefits-policy.md, expense-policy.md, onboarding-policy.md |
| Q26 | Benefits | ✅ | ✅ | ✅ | 2.11s | health-benefits-policy.md, expense-policy.md, remote-work-policy.md, it-policy.md |
| Q27 | IT | ✅ | ✅ | ✅ | 2.1s | health-benefits-policy.md, it-policy.md, expense-policy.md, pto-policy.md, onboarding-policy.md |
| Q28 | IT | ✅ | ✅ | ✅ | 2.169s | remote-work-policy.md, it-policy.md, expense-policy.md, security-policy.md |
| Q29 | CodeOfConduct | ✅ | ✅ | ✅ | 2.213s | code-of-conduct.md, remote-work-policy.md, security-policy.md |
| Q30 | OutOfScope | ✅ | ✅ | ✅ | 2.882s | pto-policy.md, performance-policy.md, code-of-conduct.md |

## Methodology

- **Groundedness**: Verified by checking that at least one source document was retrieved and cited.
- **Citation Accuracy**: Verified by confirming the retrieved sources match the expected policy document category for each question.
- **Partial Match**: Key terms from the gold answer checked against the generated answer.
- **Latency**: Measured end-to-end from request receipt to answer delivery using `time.perf_counter()`.
- Evaluation set: 30 questions covering PTO, remote work, expenses, security, conduct, performance, onboarding, training, benefits, IT, and out-of-scope detection.
