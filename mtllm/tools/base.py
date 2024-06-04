class Tool:
    description: str = "Description of the tool"
    inputs: list[tuple[str, str, str]] = [("input1", "str", "Input 1 description")]
    output: tuple[str, str] = ("str", "Output description")

    def forward(self, input1: str) -> str:
        raise NotImplementedError
    
    def get_function(self):
        return self.forward


import wikipedia   

class wikipedia(Tool):
    description: str = "Get the summary of a Wikipedia article"
    inputs: list[tuple[str, str, str]] = [("title", "str", "Title of the Wikipedia article")]
    output: tuple[str, str] = ("str", "Summary of the Wikipedia article")

    def forward(self, title: str) -> str:
        return wikipedia.summary(title)
    
