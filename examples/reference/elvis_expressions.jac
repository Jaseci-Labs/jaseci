with entry{

    data = {
        'username': 'john_doe',
        'email': 'john.doe@example.com',
        'timezone': 'UTC'};

    # Using the Elvis expression to get the 'language' configuration, with a default value of 'english' if not present
    user_language = data.get('language') ?: 'english';

    print(f"User's preferred language: {user_language}");
}