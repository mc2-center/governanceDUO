# Pre-refactor golden baselines

Frozen outputs of the builders as they stood at `caa1590`, before the model
refactor (`plans/model_refactor.md`). Phase 3 diffs the `authorizer_v1`
projection against these. The only differences allowed are `Inherited` →
`Inferred`, the added team grants, and approvals the old builder filtered out.

| File | Produced by |
|---|---|
| `governance_graph.ttl` | `make governance-graph` (`GOVERNANCE_GRAPH_AS_OF=1767225600000`) |
| `derivation_policy.ttl` | `make derivation-policy` (example inputs) |
| `sync_governance.ttl` | `sync_governance_graph.py syn50000001` against `check_sync_governance.py`'s fake Synapse client and fixture |

Don't regenerate these. They record the old behaviour, and the builders that
produced them are removed in Phase 2.
