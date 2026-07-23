import { z } from "zod";

const BaseIntent = z.object({
  confidence: z.number().min(0).max(1).describe("LLM's confidence (0.0 - 1.0) in this intent."),
});

export const TypeTextIntent = BaseIntent.extend({
  action: z.literal("type_text"),
  text: z.string().describe("Exact text to insert, properly capitalized and punctuated."),
});

export const PressKeyIntent = BaseIntent.extend({
  action: z.literal("press_key"),
  keys: z.string().describe("Talon-formatted key string (e.g., 'ctrl-c', 'enter', 'shift-down')."),
});

export const RunCliIntent = BaseIntent.extend({
  action: z.literal("run_cli"),
  command: z.string().describe("The exact bash/zsh command to execute."),
  background: z.boolean().default(false).describe("Run command in background."),
});

export const McpToolIntent = BaseIntent.extend({
  action: z.literal("mcp_tool"),
  server_name: z.string().describe("Name of the MCP server (e.g., 'codebase-memory-mcp')."),
  tool_name: z.string().describe("Name of the tool to execute."),
  arguments: z.record(z.any()).describe("JSON object containing required tool arguments."),
});

export const ComputerUseIntent = BaseIntent.extend({
  action: z.literal("computer_use"),
  operation: z.enum(["click", "double_click", "right_click", "scroll_up", "scroll_down", "move"]),
  x: z.number().int().optional().describe("Absolute X coordinate."),
  y: z.number().int().optional().describe("Absolute Y coordinate."),
});

export const EditorActionIntent = BaseIntent.extend({
  action: z.literal("editor_action"),
  operation: z.enum(["format_document", "rename_symbol", "go_to_definition", "find_references", "save"]),
});

// Discriminated union based on the 'action' field
export const VoiceAction = z.discriminatedUnion("action", [
  TypeTextIntent,
  PressKeyIntent,
  RunCliIntent,
  McpToolIntent,
  ComputerUseIntent,
  EditorActionIntent,
]);

export const ParsedVoiceCommand = z.object({
  original_transcript: z.string().describe("The raw, unedited speech transcript."),
  intents: z.array(VoiceAction).describe("Ordered sequence of executable actions derived from speech."),
});

export type ParsedVoiceCommandType = z.infer<typeof ParsedVoiceCommand>;
export type VoiceActionType = z.infer<typeof VoiceAction>;
