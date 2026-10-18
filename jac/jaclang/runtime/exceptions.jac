import from uuid { UUID }


obj MissingAnchorError(ValueError) {
    has anchor_id: str;

    def __str__ -> str;
}


obj WriteConflict(Exception) {
    has anchor_id: UUID,
        expected_version: int = -1,
        actual_version: int = -1,
        siblings: (list[any] | None) = None;

    def postinit;
    def message -> str;
}


obj ReadOnlyRetry(WriteConflict) {
    has unit_key: str = '';

    def message -> str;
}


obj TransactionLost(WriteConflict) {
    def message -> str;
}

impl MissingAnchorError.__str__ -> str {
    return (
        f"Anchor {self.anchor_id} does not exist in the anchor store "
        "(was the data store reset or migrated?)"
    );
}


impl WriteConflict.postinit {
    super.init(self.message());
}

impl WriteConflict.message -> str {
    return (
        f"WriteConflict: anchor {self.anchor_id} changed concurrently "
        f"(expected v{self.expected_version}, found v{self.actual_version})"
    );
}


impl ReadOnlyRetry.message -> str {
    return (
        f"ReadOnlyRetry: unit {self.unit_key or '<anonymous>'} wrote inside "
        'a read-only snapshot; re-run it at SERIALIZABLE'
    );
}


impl TransactionLost.message -> str {
    return (
        'TransactionLost: the transaction was rolled back and its writes '
        'cannot be replayed; re-run the unit'
    );
}
