# Detailed Explanation on littleX test cases.

To write test cases in **JacLang**, create a file with the extension `.test.jac`. This file should reside in the same context as the module or function you intend to test.

Within the `.test.jac` file, you can define test cases for specific functions. Use the `assert` statement to verify the expected outcomes and ensure the correctness of your code logic.

## visit_profile function

In Jaclang LittleX, to visit a user profile, a walker can be spawned starting from the root node. This walker navigates the graph to access and return the desired profile object.

To verify the correctness of the visit profile functionality, you can use Python’s built-in `isinstance()` function to ensure that the returned object is an instance of the `Profile` class.

Example:

```Jac
test visit_profile {
    root spawn visit_profile();
    profile = [root --> (`?Profile)][0];
    assert isinstance(profile, Profile); 
}
```
## update_profile function

To update a profile in LittleX, it is not necessary to spawn the walker from the root node. Instead, you can directly navigate to the desired `Profile` node from the `root`, and then spawn the `update_profile` walker from that node.

This approach allows for modifying attributes such as the username. The change can be verified using an `assert` statement to confirm that the update was successful.

Example:

```Jac
test update_profile {
    profile = [root --> (`?Profile)][0];
    profile spawn update_profile(
        new_username = "test_user",
    ); 
    assert profile.username == "test_user";
}
```