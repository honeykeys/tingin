def unwrap(rto):
    """Unwrap RunToolOutput → ToolOutput, raising on error."""
    if rto.root.ok:
        return rto.root.output
    raise RuntimeError(f"tool error: {rto.root.error}")


def payload(rto, model):
    """Unwrap and parse the contract_payload into a Pydantic model."""
    out = unwrap(rto)
    return model.model_validate(out.metadata["contract_payload"])
