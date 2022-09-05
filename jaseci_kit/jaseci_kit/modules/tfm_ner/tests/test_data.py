# flake8: noqa
test_train_config = {"training_parameters": {"EPOCHS": 50}}

test_model_config = {"model_parameters": {"model_save_path": "modeloutput1"}}


test_predict_input = {
    "text": "you can call me joe and my current place is on plymouth road"
}
test_predict_output = [
    {
        "entity_text": "joe",
        "entity_value": "name",
        "conf_score": 0.8819457292556763,
        "start_pos": 16,
        "end_pos": 19,
    },
    {
        "entity_text": "plymouth road",
        "entity_value": "address",
        "conf_score": 0.9251362085342407,
        "start_pos": 47,
        "end_pos": 60,
    },
]
test_training_data = [
    "my name is [Shawn](name)",
    "[Jemmott](name) is my name",
    "I'm [Juan](name)",
    "Everyone call me by the name [Katryn](name)",
    "You can call me [Spence](name)",
    "My mother give me the name [marks](name)",
    "I live in [482 Mandela Avenue](address)",
    "[Sea Street](address) is where I reside",
    "my address is [Guyana](address)",
    "My name is [Yiping](name)",
    "They call me [Kang](name)",
    "[lot 1 pineapple street](address) is where i live",
    "You see how far [beverly hills](address) is that is where i live",
    "Around [church road](address)",
    "I am located at [rob street](address)",
    "I does live in [grove](address)",
    "I reside in [Japan](address)",
    "I'm located around [pun trench](address)",
    "I live at the [Palms](address)",
    "my name is [jason](name) and i live in [mars](address)",
    "i live in [space](address) and they call me [jack](name)",
    "I'm [eldon](name) and i reside in [lot 2 queen street](address)",
    "I currently live in [Georgetown](address), I'm [Ashish](name)",
    "I'm [Satesh](name) and I reside around [Semple Street](address)",
    "My name is [Katryn Persaud](name) and I live in [Europe](address)",
]
