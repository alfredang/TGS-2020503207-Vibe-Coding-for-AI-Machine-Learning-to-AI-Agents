# Multi-Agent SDK Comparison

> Step 7 template. Fill in every blank from your own runs — fabricated numbers
> are not assessable evidence. Keep this file as evidence for the practical
> assessment.

Same architecture (routing coordinator over narrow specialists) built twice.

## Test requests
1. "What is the weather in Singapore?"    (expect weather specialist)
2. "What time is it in Tokyo?"            (expect time specialist)
3. "What is the weather on Mars?"         (expect graceful error)
4. "Tell me about Singapore."             (ambiguous - observe routing)

## Results

| Criterion | OpenAI Agents SDK | Google ADK |
|---|---|---|
| Correct routing (of 4) | _/4 | _/4 |
| Median reply latency | _ s | _ s |
| Lines of setup code | _ | _ |
| Conversation state | Passed in as input list | Held by SessionService |
| Who answered | `result.last_agent.name` | `event.author` |
| Structured output | `output_type=` | `output_schema=` |
| Built-in tracing | Yes, hosted dashboard | Yes, via `adk web` |

## Findings
- Routing: ...
- Latency: ...
- Developer experience: ...
- Failure handling: ...

## Conclusion
Use the OpenAI Agents SDK when ...
Use Google ADK when ...
