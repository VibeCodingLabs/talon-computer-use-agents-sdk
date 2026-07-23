# Voice Computer Use Agents SDK

An open-source, extensible SDK bridging natural human dictation to deterministic OS and IDE control.

## Intent
Traditional voice coding and OS control relies on rigid, memorized grammars. This SDK flips the paradigm by leveraging ultra-fast LLM inference (Groq/Llama 3) and structured generation (Instructor/Pydantic/Zod) to map **natural speech** directly into executable computer intents. 

Our goal is to build the ultimate accessibility and "vibe coding" layer for Linux and beyond. By talking naturally to your machine, you generate validated JSON schemas that execute perfectly typed text, CLI commands, and Model Context Protocol (MCP) tool calls.

## Architecture
The SDK decoupled into four plug-and-play layers, entirely bypassing the need for closed-source or legacy dictation software:

1. **The Ears (STT):** Pluggable audio capture (Deepgram, Whisper, Vapi).
2. **The Brain (Parser):** Auto-healing Pydantic schema validation via Instructor.
3. **The Voice (TTS):** Instant audio feedback (Kokoro, ElevenLabs).
4. **The Hands (Executors):** Native Wayland/X11 automation (`wtype`/`ydotool`) and Agentic MCP tool routing.

## Quick Start
*Documentation pending runtime stabilization.*
