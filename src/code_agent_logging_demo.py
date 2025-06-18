#!/usr/bin/env python3

from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import LiteLLMModel

#
# Setup for logging, LangFuse
#
import dotenv
import os
dotenv.load_dotenv()

import os
import base64

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_PRIVATE_KEY")
LANGFUSE_AUTH = base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://us.cloud.langfuse.com/api/public/otel" # US data region
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

#
# Setup for logging, open telemetry
#

from opentelemetry.sdk.trace import TracerProvider

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)

#
# Setup for logging, done
#



search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]
additional_authorized_imports = []

model = LiteLLMModel(model_id="ollama_chat/qwen3:8b", api_base="http://127.0.0.1:11434")
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=additional_authorized_imports,
    max_steps=5
)

answer = agent.run("What events are happening in Pokemon GO today?")
print(f"Agent returned answer: {answer}")
