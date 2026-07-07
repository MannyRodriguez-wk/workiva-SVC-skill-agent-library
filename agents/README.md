# Drop an agent config here

Add a YAML file: `agents/my-agent_agent.yaml`

**Copy-paste starter:**

```yaml
id: my-agent
name: My Agent
owner: svc
purpose: One sentence — what this agent does.
status: poc

skills:
  - skills/stop-slop

data_boundaries:
  reads:
    - Files the user provides in-session
  writes:
    - Draft outputs (local)
  prohibited:
    - No customer PII
    - No secrets in the YAML

required_environment_variables: []

review_requirements:
  human_review_required: true
```

No credentials in the file — ever. Open a PR. See [CONTRIBUTING.md](../CONTRIBUTING.md).
