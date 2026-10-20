import from "@jac/mobui" {
    View,
    Text,
    StatusBar,
    ActivityIndicator,
    Pressable,
    useWindowDimensions
}

glob TAB_TITLES: dict[str, str] = {
         "feed": "Home",
         "scores": "Ninja Scores",
         "explore": "Explore",
         "channels": "Channels",
         "profile": "Profile"
     };

def:pub JacYacMobile(embedded: bool = False) -> JsxElement;
