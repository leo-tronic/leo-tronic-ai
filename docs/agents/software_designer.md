## Designing
- Use mermaid md charts for simple, local charting, i.e. for simple process flows or low-level designs
- Use lucid MCP, with permission, for creating AWS / architecture diagrams

## Embedding Lucid Diagrams in Confluence

⚠️ **CRITICAL**: MCP Confluence tools strip XML macro syntax when updating pages. Use direct REST API instead.

**Correct Approach:**
1. Create page with MCP Confluence tool
2. Update page with direct REST API + basic auth: `curl -u "email:token"`
3. Use `lucidchart` macro (NOT `lucid`) with full parameters

**Lucidchart Macro Template:**
```xml
<ac:structured-macro ac:name="lucidchart" ac:schema-version="1" data-layout="default">
  <ac:parameter ac:name="viewerType">editor</ac:parameter>
  <ac:parameter ac:name="installationPlatform">CLOUD</ac:parameter>
  <ac:parameter ac:name="embedVersion">latest-version</ac:parameter>
  <ac:parameter ac:name="lucidProduct">lucidchart</ac:parameter>
  <ac:parameter ac:name="documentId">YOUR_DIAGRAM_ID</ac:parameter>
  <ac:parameter ac:name="width">500</ac:parameter>
  <ac:parameter ac:name="height">500</ac:parameter>
  <ac:parameter ac:name="alignment">left</ac:parameter>
</ac:structured-macro>
```

**REST API Update Example:**
```bash
curl -X PUT -u "email:token" -H "Content-Type: application/json" \
  -d '{"id":"pageId","version":{"number":2},"title":"Page","type":"page","status":"current","body":{"storage":{"value":"<h1>Title</h1><ac:structured-macro...>","representation":"storage"}}}' \
  "https://drivewealth.atlassian.net/wiki/api/v2/pages/pageId"
```

**Common Issues:**
- 403: Use basic auth `-u "email:token"`, not Bearer token
- "Error loading extension": Wrong macro name or missing parameters
- 400 (id/status null): Include both fields in JSON body