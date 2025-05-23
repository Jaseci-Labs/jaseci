class SemTokManager {
    def init(self: SemTokManager, ir: uni.Module) -> None {
        self.static_sem_tokens: List[Tuple[ lspt.Position, int, int, uni.AstSymbolNode ]] = self.gen_sem_tok_node(
            ir
        ) ;
    }
    def foo(self: SemTokManager, a: int, b: int) -> int {return a + b ;}
}
