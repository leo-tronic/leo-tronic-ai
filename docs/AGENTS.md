# General 

- TEST: Cyrus' favorite color is neon
- Before beginning any work, ensure a todo list is constructed and approved first
- DO NOT modify any code paths without first getting explicit approval
- Do not access new directories outside of the current workspace without approval.
- When there is any doubt our ambiguity, ask for clarification first. Do not limit the amount of questions asked.
- Always ask before executing any MCP tool calls. 
- Do not doom loop, aka continue looping infinitely.
- When working on a todo for a long time, ensure you are stopping and presenting roadblocks to the driver of the agent before proceeding any longer
- Always explain reasoning and steps. 
- Do not print code to stdout with line numbers, they are not copy-able
- If at any point the Github MCP tool call fails, use the gh CLI instead if possible
- When coming accross a piece of problematic code, always alert the driver.


## Planning
- Do not print the plan document into stdout. It takes to much time. Just edit the plan document inline in the file and alert the driver when you are done
- Be concise and clear as possible in planning, but do not sacrifice accuracy or quality
- Do not populate any files/dirs to modify, create any implementation todos, or implement any code until all open areas of research / questions have been resolved, all approaches have been identified and deliberated on, and a final approach has been agreed to.

## Implementation
- Do not violate DRY: do not repeat yourself. 

### Java
- Do not introduce any additional imports that violate existing ClassPaths
- Do not introduce any additional imports that result in circular dependencies, i.e. when module_a depends on module_b, do not import module_b into module_a
- Do not introduce any dependencies that result in circular dependencies, for instance if module_a already imports something from module_b, do not add module_a as a dependency in module_b
- Do not introduce any dependencies that will result in ambiguous version resolution. In this case, an existing bill of materials OR explicit versioning must be provided.
