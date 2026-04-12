# RAG Evaluation Results

## Summary

| Metric | Score |
|--------|-------|
| **Groundedness** | 100.0% |
| **Citation Accuracy** | 100.0% |
| **Partial Match (Gold)** | 96.7% |
| **Latency p50** | 2.760s |
| **Latency p95** | 5.134s |
| **Latency avg** | 3.363s |
| **Questions evaluated** | 30 |

## Per-Question Results

| ID | Category | Grounded | Citation | Partial Match | Latency | Sources |
|----|----------|----------|----------|---------------|---------|---------|
| Q01 | PTO | ✅ | ✅ | ✅ | 17.963s | pto-policy.md, health-benefits-policy.md, onboarding-policy.md |
| Q02 | PTO | ✅ | ✅ | ✅ | 4.687s | pto-policy.md |
| Q03 | PTO | ✅ | ✅ | ✅ | 2.8s | remote-work-policy.md, pto-policy.md, onboarding-policy.md, health-benefits-policy.md |
| Q04 | PTO | ✅ | ✅ | ✅ | 2.733s | pto-policy.md, training-policy.md, onboarding-policy.md |
| Q05 | PTO | ✅ | ✅ | ✅ | 3.106s | pto-policy.md, performance-policy.md, remote-work-policy.md, expense-policy.md |
| Q06 | RemoteWork | ✅ | ✅ | ✅ | 2.983s | remote-work-policy.md, health-benefits-policy.md |
| Q07 | RemoteWork | ✅ | ✅ | ✅ | 2.912s | remote-work-policy.md, it-policy.md |
| Q08 | RemoteWork | ✅ | ✅ | ✅ | 2.69s | expense-policy.md, remote-work-policy.md, health-benefits-policy.md |
| Q09 | RemoteWork | ✅ | ✅ | ✅ | 3.058s | remote-work-policy.md, health-benefits-policy.md, training-policy.md |
| Q10 | Expense | ✅ | ✅ | ✅ | 2.788s | expense-policy.md, performance-policy.md |
| Q11 | Expense | ✅ | ✅ | ✅ | 3.8s | expense-policy.md |
| Q12 | Expense | ✅ | ✅ | ✅ | 2.911s | expense-policy.md, training-policy.md, health-benefits-policy.md |
| Q13 | Expense | ✅ | ✅ | ✅ | 2.549s | expense-policy.md, training-policy.md |
| Q14 | Security | ✅ | ✅ | ✅ | 3.127s | security-policy.md, remote-work-policy.md |
| Q15 | Security | ✅ | ✅ | ✅ | 1.866s | security-policy.md, remote-work-policy.md, it-policy.md, health-benefits-policy.md |
| Q16 | Security | ✅ | ✅ | ✅ | 1.88s | security-policy.md, it-policy.md, remote-work-policy.md, pto-policy.md |
| Q17 | CodeOfConduct | ✅ | ✅ | ✅ | 5.134s | code-of-conduct.md, expense-policy.md |
| Q18 | Performance | ✅ | ✅ | ❌ | 4.602s | performance-policy.md, code-of-conduct.md |
| Q19 | Performance | ✅ | ✅ | ✅ | 3.36s | performance-policy.md |
| Q20 | Onboarding | ✅ | ✅ | ✅ | 2.435s | onboarding-policy.md, pto-policy.md, performance-policy.md |
| Q21 | Onboarding | ✅ | ✅ | ✅ | 2.359s | onboarding-policy.md, health-benefits-policy.md |
| Q22 | Training | ✅ | ✅ | ✅ | 2.8s | training-policy.md, expense-policy.md |
| Q23 | Training | ✅ | ✅ | ✅ | 1.797s | training-policy.md |
| Q24 | Benefits | ✅ | ✅ | ✅ | 2.584s | health-benefits-policy.md, performance-policy.md |
| Q25 | Benefits | ✅ | ✅ | ✅ | 2.583s | health-benefits-policy.md, expense-policy.md, training-policy.md |
| Q26 | Benefits | ✅ | ✅ | ✅ | 2.718s | health-benefits-policy.md, training-policy.md |
| Q27 | IT | ✅ | ✅ | ✅ | 2.116s | it-policy.md, remote-work-policy.md, security-policy.md, onboarding-policy.md |
| Q28 | IT | ✅ | ✅ | ✅ | 2.131s | remote-work-policy.md, it-policy.md, security-policy.md |
| Q29 | CodeOfConduct | ✅ | ✅ | ✅ | 2.405s | code-of-conduct.md, security-policy.md |
| Q30 | OutOfScope | ✅ | ✅ | ✅ | 1.999s | expense-policy.md |

## Methodology

- **Groundedness**: Verified by checking that at least one source document was retrieved and cited.
- **Citation Accuracy**: Verified by confirming the retrieved sources match the expected policy document category for each question.
- **Partial Match**: Key terms from the gold answer checked against the generated answer.
- **Latency**: Measured end-to-end from request receipt to answer delivery using `time.perf_counter()`.
- Evaluation set: 30 questions covering PTO, remote work, expenses, security, conduct, performance, onboarding, training, benefits, IT, and out-of-scope detection.
