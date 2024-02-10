from jaclang.plugin.feature import JacFeature as jac

user_language = None
preferred_language = jac.elvis(user_language, "english")
print(preferred_language)
