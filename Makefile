.PHONY: help install clean test langchain-install langchain-version langchain-serve \
		bedrock-list-models bedrock-list-foundation-models bedrock-invoke-model \
		bedrock-list-agents bedrock-list-knowledge-bases bedrock-get-model \
		langchain-api-key langchain-tracing bedrock-configure docs

# Default target
help:
	@echo "Available targets:"
	@echo ""
	@echo "Setup:"
	@echo "  install                    - Install project dependencies"
	@echo "  clean                      - Clean temporary files and caches"
	@echo ""
	@echo "LangChain Commands:"
	@echo "  langchain-install          - Install LangChain and related packages"
	@echo "  langchain-version          - Show LangChain version"
	@echo "  langchain-serve            - Start LangChain server (LangServe)"
	@echo "  langchain-api-key          - Configure LangChain API key"
	@echo "  langchain-tracing          - Enable LangSmith tracing"
	@echo ""
	@echo "AWS Bedrock Commands:"
	@echo "  bedrock-configure          - Configure AWS credentials for Bedrock"
	@echo "  bedrock-list-models        - List all available Bedrock models"
	@echo "  bedrock-list-foundation-models - List Bedrock foundation models"
	@echo "  bedrock-get-model          - Get details of a specific model (MODEL_ID=...)"
	@echo "  bedrock-invoke-model       - Invoke a Bedrock model (MODEL_ID=... PROMPT=...)"
	@echo "  bedrock-list-agents        - List Bedrock agents"
	@echo "  bedrock-list-knowledge-bases - List Bedrock knowledge bases"
	@echo ""
	@echo "Documentation:"
	@echo "  docs                       - Open documentation directory"
	@echo ""
	@echo "Testing:"
	@echo "  test                       - Run tests"

# Setup targets
install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install langchain langchain-community langchain-aws boto3

clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov

# LangChain targets
langchain-install:
	@echo "Installing LangChain packages..."
	pip install langchain langchain-community langchain-core langchain-openai
	pip install langserve langsmith langgraph

langchain-version:
	@echo "LangChain version:"
	python -c "import langchain; print(langchain.__version__)"

langchain-serve:
	@echo "Starting LangChain server..."
	@echo "Note: This requires a LangServe application setup"
	@echo "Run: langchain serve"

langchain-api-key:
	@echo "Setting up LangChain API key..."
	@echo "Export your API key:"
	@echo "  export LANGCHAIN_API_KEY=your-api-key-here"
	@echo "Or add it to your .env file"

langchain-tracing:
	@echo "Enabling LangSmith tracing..."
	@echo "Set the following environment variables:"
	@echo "  export LANGCHAIN_TRACING_V2=true"
	@echo "  export LANGCHAIN_API_KEY=your-api-key-here"
	@echo "  export LANGCHAIN_PROJECT=your-project-name"

# AWS Bedrock targets
bedrock-configure:
	@echo "Configuring AWS credentials for Bedrock..."
	aws configure
	@echo "Make sure your AWS account has Bedrock access"

bedrock-list-models:
	@echo "Listing all Bedrock models..."
	aws bedrock list-foundation-models --query 'modelSummaries[*].[modelId,modelName,providerName]' --output table

bedrock-list-foundation-models:
	@echo "Listing Bedrock foundation models..."
	aws bedrock list-foundation-models --output json | jq '.modelSummaries[] | {modelId, modelName, providerName}'

bedrock-get-model:
	@echo "Getting model details for $(MODEL_ID)..."
	@if [ -z "$(MODEL_ID)" ]; then \
		echo "Error: MODEL_ID not set. Usage: make bedrock-get-model MODEL_ID=anthropic.claude-v2"; \
		exit 1; \
	fi
	aws bedrock get-foundation-model --model-identifier $(MODEL_ID)

bedrock-invoke-model:
	@echo "Invoking Bedrock model $(MODEL_ID)..."
	@if [ -z "$(MODEL_ID)" ]; then \
		echo "Error: MODEL_ID not set. Usage: make bedrock-invoke-model MODEL_ID=anthropic.claude-v2 PROMPT='Hello'"; \
		exit 1; \
	fi
	@if [ -z "$(PROMPT)" ]; then \
		echo "Error: PROMPT not set. Usage: make bedrock-invoke-model MODEL_ID=anthropic.claude-v2 PROMPT='Hello'"; \
		exit 1; \
	fi
	@echo '{"prompt": "$(PROMPT)", "max_tokens_to_sample": 200}' > /tmp/bedrock_input.json
	aws bedrock-runtime invoke-model \
		--model-id $(MODEL_ID) \
		--body file:///tmp/bedrock_input.json \
		/tmp/bedrock_output.json
	@cat /tmp/bedrock_output.json
	@rm -f /tmp/bedrock_input.json /tmp/bedrock_output.json

bedrock-list-agents:
	@echo "Listing Bedrock agents..."
	aws bedrock-agent list-agents --query 'agentSummaries[*].[agentId,agentName,agentStatus]' --output table

bedrock-list-knowledge-bases:
	@echo "Listing Bedrock knowledge bases..."
	aws bedrock-agent list-knowledge-bases --query 'knowledgeBaseSummaries[*].[knowledgeBaseId,name,status]' --output table

# Documentation
docs:
	@echo "Opening documentation..."
	@if [ -d "docs" ]; then \
		cd docs && ls -la; \
	else \
		echo "Documentation directory not found"; \
	fi

# Testing
test:
	@echo "Running tests..."
	@echo "Note: Add your test commands here"
	@echo "Example: pytest tests/"
