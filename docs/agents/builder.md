# Building
- The basis for building every single feature is going to be a document in either:
  - leo-tronic-ai/docs/features/ if it is a feature
  - leo-tronic-ai/docs/bugs/ if it is a bug
  - leo-tronic-ai/docs/designs/ if it is a new design
- This would be an instantiation of one of the templates:
  - leo-tronic-ai/docs/templates/feature.md if it is a feature
  - leo-tronic-ai/docs/templates/design.md if it is a design
- The build agent must operate on the basis of the document, and not deviate from it. If there are any questions about the document, ask for clarification.
- If a feature is small enough, it may not need a document and will be a much simpler document outlining requirements
- This document must be continually updated by the build agent. Here are the cases in which the build agent must update the document:
  - When there are any changes to the requirements, design, or implementation plan
  - When there are any changes to the acceptance criteria
  - When there are any changes to the implementation steps
  - When there are major findings that were discovered during implementation or testing
  - When there were blockers / issues that were resolved, and the resolution of those blockers / issues

## Build Principles
- Do not violate DRY: do not repeat yourself.
  raise it as a blocker, do not extrapolate from incomplete information

## Implicit Acceptance Crtieria for all PRs
- Ensure there are no merge conflicts on PRs
  - If resolving conflicts is unclear, ask for clarification
- Ensure there are are no build check errors
  - If access to build logs are needed, request them. do not extrapolate from incomplete info

## Implicit acceptance criteria for all changes
- Ensure all source code files were formatted properly
- Ensure the source code compiles locally without errors
- Ensure the source code passes all tests unless explicitly overridden
- All changes must have an accompanying test case associated with it

## Java
- Do not introduce any additional imports that violate existing ClassPaths
- Do not introduce any additional imports that result in circular dependencies, i.e. when module_a depends on module_b, do not import module_b into module_a
- Do not introduce any dependencies that result in circular dependencies, for instance if module_a already imports something from module_b, do not add module_a as a dependency in module_b
- Do not introduce any dependencies that will result in ambiguous version resolution. In this case, an existing bill of materials OR explicit versioning must be provided.
