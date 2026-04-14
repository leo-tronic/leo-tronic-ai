# Debugging

## Preferred Tools:
- When possible, use file-based stdout logs
- For deployed environments, leverage Grafana MCP

---

## Local Debugging

Apps in this ecosystem (e.g. `drivewealth-bo-api`) use **log4j2** for logging.

### Activating Local File-Based Logging
- Pass the JVM arg: `-Dlog4j2.configurationFile=classpath:log4j2-local.xml`
- Logs will be written to `logs/bo-api.log` by default (configurable via `LOG_FILE_PATH` env var)
- The local config writes to both a rolling file and stdout (console appender)

### Reading Local Logs
- Use the `Read` tool to read log files from the path above
- Logs are plain-text in local mode (not JSON), so they are human/agent-readable directly
- A separate `StatsConsole` logger emits metrics/stats lines — look for those when diagnosing performance

---

## Remote / Deployed Debugging

Use **Grafana MCP** for all deployed environment debugging. Do not attempt to SSH into pods or nodes.

### Grafana Datasources

| Purpose | Datasource Name |
|---|---|
| Application logs (all environments) | `grafanacloud-drivewealth-logs` |
| AWS CloudWatch metrics | `awsCloudWatch` |
| EKS / Cloud 2.0 app metrics | `Drivewealth-Metrics` |
| ROSA / OpenShift / Cloud 1.0 app metrics | `victoriaMetrics-app-prod` |

### Log Format (Deployed)
- Deployed apps emit logs as **JSON to stdout**, using `JsonTemplateLayout`
- Key logger namespaces to filter on:
  - `com.drivewealth.backoffice`
  - `com.drivewealth.rest_common`
  - `com.drivewealth.ss.common`
- Use LogQL label selectors to scope queries by app/namespace/pod before filtering on log content

### Metrics
- For EKS (Cloud 2.0) apps, query `Drivewealth-Metrics` with PromQL
- For ROSA/OpenShift (Cloud 1.0) apps, query `victoriaMetrics-app-prod` with PromQL
- For AWS-level metrics (Lambda invocations, SQS depth, DynamoDB throttles, etc.), query `awsCloudWatch`

---

## AWS Resources

Auth is handled via AWS SSO. Before making any AWS CLI calls:

```
aws sso login
# or use the helper alias:
aws_login <profile_name_from_aws_conf>
```

Profile names are defined in `~/.aws/config`. Always confirm the correct profile with the user before running commands.

### DynamoDB
- Endpoint: `https://dynamodb.us-east-1.amazonaws.com`
- Use `aws dynamodb` CLI commands to scan/query tables
- Always scope queries with `--limit` to avoid large result sets
- Example: `aws dynamodb scan --table-name <table> --limit 10 --profile <profile>`

### SQS
- Use `aws sqs` CLI commands to inspect queue depth, receive messages, or purge
- Example: `aws sqs get-queue-attributes --queue-url <url> --attribute-names All --profile <profile>`

### S3
- Multiple buckets in use: compliance docs, instrument images, BOD files, allocation storage, etc.
- Use `aws s3 ls` and `aws s3 cp` for inspection and retrieval
- Always confirm bucket name and path with user before any write/delete operations

### KMS
- Endpoint: `https://kms.us-east-1.amazonaws.com`
- Use `aws kms` CLI for key inspection only (e.g. `describe-key`, `list-keys`)
- Do not attempt decrypt/encrypt operations without explicit user instruction

### CloudFront
- Distribution IDs are environment-specific
- Use `aws cloudfront` CLI to inspect distributions or create invalidations when instructed

---

## Postgres / Aurora (Babelfish)

> **IMPORTANT: The agent must NOT run Postgres queries directly.**

The Aurora Babelfish endpoint is at:
```
dwdev-aurora-babelfish.cluster-csefnakly5ig.us-east-1.rds.amazonaws.com:5432
```
Database: `post_trade`

**Protocol:**
1. Formulate the SQL query based on the debugging context
2. Present the query to the user and ask them to run it
3. Wait for the user to paste back the results
4. Interpret the results and continue debugging

Never attempt to connect to the database directly or run queries via CLI tools.

---

## Other Services (Awareness Only)

These services are in use across the ecosystem. The agent should be aware of them for context but should not attempt to interact with them directly unless given explicit tooling/access:

| Service | Notes |
|---|---|
| **Redis (Jedis)** | Used for caching. Local at `localhost:6379`. Inspect via `redis-cli` if locally available. |
| **Kafka (Confluent Cloud)** | Used for streaming. Do not attempt to produce/consume without explicit instruction. |
| **ActiveMQ** | Used for messaging and NearCache invalidation. Do not connect without explicit instruction. |

---

## Deployment Environments

| Environment | Platform | Notes |
|---|---|---|
| `local` | Developer machine / Docker | Uses `application-local.properties`; log4j2-local.xml for logs |
| `dev` | EKS or ROSA | Logs in Grafana; use dev-scoped label selectors |
| `qa` | EKS or ROSA | Same as dev |
| `uat` | EKS or ROSA | Same as dev |
| `prod` | EKS (Cloud 2.0) and/or ROSA (Cloud 1.0) | Extra care required; confirm all actions with user |

- **EKS / Cloud 2.0**: use `Drivewealth-Metrics` for metrics, `grafanacloud-drivewealth-logs` for logs
- **ROSA / OpenShift / Cloud 1.0**: use `victoriaMetrics-app-prod` for metrics, `grafanacloud-drivewealth-logs` for logs

---

## General Agent Rules for Debugging

- Always start by scoping the problem: environment, service name, time range, and error signature
- For remote logs, use Grafana MCP — do not guess at log content
- For AWS resources, always confirm the correct profile and region before running CLI commands
- For database investigations, formulate queries and ask the user to run them — never connect directly
- If build logs or CI outputs are needed and inaccessible, raise it as a blocker — do not extrapolate
- Do not doom loop: if a debugging path yields no results after 2–3 attempts, stop and report findings to the user

---

## Hypothesis vs. Root Cause

A hypothesis is not a root cause. These must never be conflated.

- A **hypothesis** is a plausible explanation for observed behavior, formed from log evidence, code reading, and system knowledge. It may be wrong.
- A **root cause** is only confirmed when:
  1. A system expert with direct knowledge of the component explicitly agrees it is the cause, AND
  2. Hard evidence (e.g. configuration payload, database record, runtime behavior) directly supports it

**Rules:**
- Never write a hypothesis into the "Root Cause" section of a bug doc — label it as a hypothesis
- Do not propose solutions based on an unconfirmed hypothesis
- When a hypothesis is invalidated (by data, expert input, or logic), mark it as such and move on
- If two or more hypotheses have been invalidated and no new lead exists, **stop and escalate to a system expert**
- When escalating, write a clear summary of what has been investigated, what has been ruled out, and what is still unknown

---

## Evidence Standards

- **Never make inferences without hard evidence.** If a conclusion is not directly supported by a log line, config value, API response, or other concrete artifact, do not state it as fact.
- **Always cite the evidence for any claim.** Every statement in an analysis must be traceable to a specific source (e.g. a log line, a file and line number, an API response body, a config value).
- **Never extrapolate from insufficient evidence.** For example, inferring "no outbound HTTP call was made" from a fast processing time is not valid — processing time alone does not prove the absence of a network call.
- **Never make assumptions.** If something is unknown, state it as unknown. Do not fill gaps with plausible-sounding explanations.
- **Label inferences explicitly.** If a statement is an inference rather than a directly observed fact, prefix it with "Inference:" and include the evidence it is based on and why the inference is being made.