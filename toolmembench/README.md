# ToolMemBench

This repository contains the ToolMemBench implementation modules and benchmark samples associated with the manuscript *ToolMemBench: Evaluating Closed-Loop Memory Poisoning in Tool-Using Large Language Model Agents*.

## Contents

- `toolmembench/agent/`: scenario agents and tool-call handling.
- `toolmembench/defense/`: memory-risk and tool-call defense components.
- `toolmembench/eval/`: evaluation predicates and metrics.
- `toolmembench/llm/`: model API adapter.
- `toolmembench/memory/`: memory backend implementations.
- `toolmembench/tools/`: deterministic mock business tools.
- `toolmembench/benchmark/`: benchmark samples listed below.

| Benchmark file | Samples | Scope |
| --- | ---: | --- |
| `closed_loop_v2_120.jsonl` | 120 | Main Email/Finance benchmark |
| `closed_loop_crm_v1_40.jsonl` | 40 | CRM scenario |
| `closed_loop_calendar_v1_40.jsonl` | 40 | Calendar scenario |
| `closed_loop_devops_v1_40.jsonl` | 40 | DevOps scenario |
| `closed_loop_finance_lowrisk_v1_30.jsonl` | 30 | Low-risk Finance control |
| `closed_loop_normal_business_v1_120.jsonl` | 120 | Normal-business control |

