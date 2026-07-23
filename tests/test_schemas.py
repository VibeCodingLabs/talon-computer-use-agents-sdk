from schemas.voice_intents.voice_intents import TypeTextIntent


def test_type_text_intent_validation():
    """Ensure the Pydantic schema properly validates natural language intents."""
    intent = TypeTextIntent(confidence=0.99, text="print('hello world')")

    assert intent.action == "type_text"
    assert intent.text == "print('hello world')"
    assert intent.confidence == 0.99
