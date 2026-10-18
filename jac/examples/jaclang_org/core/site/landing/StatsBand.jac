glob _STATS: list[dict[str, any]] = [
         {"n": "1", "label": "binary", "sub": "replaces your whole toolchain"},
         {
             "n": "1",
             "label": "language",
             "sub": "for the browser, the cloud, and the metal"
         },
         {"n": "3", "label": "ecosystems", "sub": "Python, JSX, and native binary"},
         {"n": "~5×", "label": "less code", "sub": "the compiler writes the glue"},
         {
             "n": "0",
             "label": "glue artifacts",
             "sub": "no ORM, routes, YAML, serializers"
         },

     ];

def:pub StatsBand -> JsxElement;
