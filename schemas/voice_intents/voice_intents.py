from typing import List, Literal, Optional, Union, Dict, Any
from pydantic import BaseModel, Field


class BaseIntent(BaseModel):
    """Base model for all parsed voice intents."""

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="The LLM's confidence that this intent matches the user's spoken command.",
    )


class TypeTextIntent(BaseIntent):
    """Intent to insert or type raw text (dictation)."""

    action: Literal["type_text"] = "type_text"
    text: str = Field(
        ..., description="The exact text to insert, properly capitalized and punctuated."
    )


class PressKeyIntent(BaseIntent):
    """Intent to press a specific keyboard shortcut or key combination."""

    action: Literal["press_key"] = "press_key"
    keys: str = Field(
        ..., description="Talon-formatted key string (e.g., 'ctrl-c', 'enter', 'shift-down')."
    )


class RunCliIntent(BaseIntent):
    """Intent to execute a terminal/shell command."""

    action: Literal["run_cli"] = "run_cli"
    command: str = Field(..., description="The exact bash/zsh command to execute.")
    background: bool = Field(False, description="Whether to run the command in the background.")


class McpToolIntent(BaseIntent):
    """Intent to invoke a Model Context Protocol (MCP) tool."""

    action: Literal["mcp_tool"] = "mcp_tool"
    server_name: str = Field(
        ..., description="The name of the MCP server (e.g., 'codebase-memory-mcp', 'github')."
    )
    tool_name: str = Field(..., description="The name of the tool to execute.")
    arguments: Dict[str, Any] = Field(
        default_factory=dict, description="A JSON object containing the required tool arguments."
    )


class ComputerUseIntent(BaseIntent):
    """Intent to perform a raw OS-level mouse or screen action (Linux Wayland/X11)."""

    action: Literal["computer_use"] = "computer_use"
    operation: Literal["click", "double_click", "right_click", "scroll_up", "scroll_down", "move"]
    x: Optional[int] = Field(None, description="Absolute X coordinate on the screen.")
    y: Optional[int] = Field(None, description="Absolute Y coordinate on the screen.")


class EditorActionIntent(BaseIntent):
    """Intent to perform an IDE-specific action (LSP integration)."""

    action: Literal["editor_action"] = "editor_action"
    operation: Literal[
        "format_document", "rename_symbol", "go_to_definition", "find_references", "save"
    ]


# Discriminated union of all possible intents
VoiceAction = Union[
    TypeTextIntent,
    PressKeyIntent,
    RunCliIntent,
    McpToolIntent,
    ComputerUseIntent,
    EditorActionIntent,
]


class ParsedVoiceCommand(BaseModel):
    """The root schema returned by the Instructor LLM representing the parsed transcript."""

    original_transcript: str = Field(..., description="The raw, unedited speech transcript.")
    intents: List[VoiceAction] = Field(
        ...,
        description="The ordered sequence of executable actions derived from the speech. Can contain multiple distinct intents.",
    )
