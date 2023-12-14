with entry{

  # List 
  frameworks = ["TensorFlow", "PyTorch", "Scikit-Learn", "Keras", "Theano", "MXNet"];
  popular_frameworks = [framework for framework in frameworks if framework.startswith("T")];
  print(popular_frameworks);

#   # List comprehension: Squaring numbers greater than 100 using the walrus operator
#   numbers = [90, 110, 120, 130, 140, 150];
#   squared_numbers = [num_squared for num in numbers if (num_squared := num ** 2) > 100];
#   print(squared_numbers);

  # List comprehension: Incrementing version numbers
  version_numbers = [1.0, 2.0, 3.0, 4.0];
  incremented_versions = [version + 0.1 for version in version_numbers];
  print(incremented_versions);

  # Generator expression: Multiplying by 3
  multiplied_numbers = (x * 3 for x in range(5));
  print(list(multiplied_numbers));

  # Set comprehension: Creating a set of ML tasks
  ml_tasks = {"classification", "regression", "clustering", "feature_extraction", "reinforcement_learning"};
  popular_ml_tasks = {task for task in ml_tasks};
  print(popular_ml_tasks);

#   Dict comprehension: Creating a dictionary with ML libraries and their popularity
  ml_libraries = {'TensorFlow': 90, 'PyTorch': 85, 'Scikit-Learn': 80, 'Keras': 75};
  popular_ml_libraries = {library for library in ml_libraries };
  print(popular_ml_libraries);

  # Dictionary value: Student information with AI context
  student_info = {'name': 'AI Bot', 'age': 100, 'role': 'Learning Agent'};
  print(student_info);

  # List value: Different AI models
  ai_models = ["Neural Network", "Decision Tree", "Random Forest", ["Support Vector Machine", "K-Nearest Neighbors"], "Gradient Boosting"];
  print(ai_models);

  # Tuple value: AI research coordinates
  ai_research_coordinates = (3.14, ["Deep Learning", "Natural Language Processing"], 2.71);
  print(ai_research_coordinates);

  # Set value: Unique AI algorithms
  unique_algorithms = {"Linear Regression", "Convolutional Neural Network", "K-Means Clustering"};
  print(unique_algorithms);
}
