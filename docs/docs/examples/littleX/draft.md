# Detailed Explanation on littleX test cases.

To write test cases for **littleX** in JacLang, create a file with the extension `.test.jac`. This test file should be placed in the same context or directory as the Jac module or walker you intend to test to ensure proper access to the target elements. Within the `littleX.test.jac` file, you can define test functions using the `test` keyword, followed by a descriptive name (e.g., test create_tweet). Each test should simulate a scenario where a specific function or walker is invoked and its behavior is validated.

Use the `check` statement within the test body to assert the expected outcome of the logic under test. The `check` keyword performs an assertion and will cause the test to fail if the condition is not met. This helps ensure that your logic works as intended and guards against regressions. You can use expressions like `check obj.attr == expected_value`, `check len(collection) == expected_count`, or similar validations.

Tests can include operations like updating node attributes, verifying edge relationships, and checking object states before and after the action. The structure encourages clean and modular testing aligned with the Jac programming model.

## visit_profile function

In LittleX, to visit a user profile, a walker can be spawned starting from the root node. This walker navigates the graph to access and return the desired profile object.

To verify the correctness of the `visit profile` functionality, you can use  `isinstance()` function to ensure that the returned object is an instance of the `Profile` node.

Example:

```Jac
test visit_profile {
    root spawn visit_profile();
    profile = [root --> (`?Profile)][0];
    check isinstance(profile,Profile); 
}
```
## update_profile function

To update a profile in LittleX, a `update_profile` walker can be spawn starting from the root node.inside the `update_profile` function you can change the username.

To verify the correctness of the `update_profile` function, you can check profile's username with new username.

Example:

```Jac
test update_profile {
    root spawn update_profile(
        new_username = "test_user",
    ); 
    profile = [root --> (`?Profile)][0];
    check profile.username == "test_user";
}
```

## follow_request function

The test `follow_request` function in JacLang tests whether a profile can successfully follow another `profile` using the `follow_request` walker. It first retrieves an existing Profile node from the graph connected to the `Profile`, which acts as the follower.

A new `Profile` node named "Sam" is then created to serve as the followee. The test triggers the `follow_request()` walker from the followee's node, which is assumed to internally establish a `Follow` edge from the follower to the followee. 

After this action, the test queries the graph for a `Follow` edge starting from the original profile and retrieves the connected profile. Finally, it checks that the username of the connected profile is "Sam", confirming that the follow relationship was correctly formed.

Example:

```Jac
test follow_request {
    followee = Profile("Sam");
    followee spawn follow_request();
    followee_profile = [root --> (`?Profile)-:Follow:->(`?Profile)][0];
    check followee_profile.username == "Sam";
}
```

## un_follow_request function

The test `un_follow_request` function verifies that a follow relationship can be removed between two profiles. It creates a profile named "Jonny", initiates a follow request to link it with an existing profile, and then runs an unfollow request to remove that link. The test finally checks how many follow connections remain, expecting one. This helps ensure that the `un_follow_request()` walker correctly handles the removal of follow edges in the graph.

Example:

```Jac 
test un_follow_request {
    followee = [root --> (`?Profile)-:Follow:->(`?Profile)][0]; 
    followee spawn un_follow_request();
    check len([root --> (`?Profile)-:Follow:->(`?Profile)]) == 0;
}
```

## create tweet function

The `test create_tweet` function checks whether a tweet with specific content can be created and linked to a profile. It spawns the `create_tweet()` walker with the content `"test_tweet"`in the `root`node.Then it navigates to the `Tweet` node.Then verifies that a `Tweet` node with the correct content is attached to the profile.

Example:

```Jac
test create_tweet {
    root spawn create_tweet(
        content = "test_tweet",
    ); 
    test1 = [root --> (`?Profile) --> (`?Tweet)][0];
    check test1.content == "test_tweet";
}
```

## update_tweet function

The `test update_tweet` function verifies that a tweet's content can be successfully updated. It first retrieves an existing tweet associated with the `root` node, then spawns the `update_tweet()` walker from the `tweet` node with the updated content `"new_tweet"`, and finally checks whether the tweet's content has been correctly updated.

Example:

```Jac
test update_tweet {
    tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];
    tweet1 spawn update_tweet(
        updated_content = "new_tweet",
    );
    check tweet1.content == "new_tweet";
}
```

## Remove_tweet function

The `test remove_tweet` function validates the deletion of a tweet. It first retrieves an existing tweet associated with the `root` node by traversing through the profile, then spawns the `remove_tweet()` walker from the tweet node to remove it. Finally, it checks that no tweets remain linked to the profile, confirming the tweet was successfully removed.

Example:

```Jac
test remove_tweet {
    tweet2 =  [root --> (`?Profile)--> (`?Tweet)][0];
    tweet2 spawn remove_tweet();
    check len([root --> (`?Profile) --> (`?Tweet)]) == 0;
}
```

## Like_tweet function

The `test like_tweet` function validates the ability of a profile to like a tweet. It begins by creating a tweet from the `root` node, followed by navigating to the corresponding `tweet` node. The function then spawns the `like_tweet` walker from the `tweet1` node and subsequently verifies that the username `"test_user"` is correctly associated with the `Like` relationship on the tweet.

```Jac 
test like_tweet {
    root spawn create_tweet(
        content = "test_like",
    );
    tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];
    tweet1 spawn like_tweet();
    test1 = [tweet1 -:Like:-> ][0];
    check test1.username == "test_user";
}
```

## remove_like function

The `test remove_like` function verifies the functionality of removing a like from a tweet. It retrieves an existing tweet from the `root` node, then spawns the `remove_like` walker from the `tweet1` node. The function subsequently checks that the `Like` relationship is successfully removed by confirming that the length of the associated likes is zero.

Example:

```Jac
test remove_like {
    tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];
    tweet1 spawn remove_like();
    check len([tweet1 -:Like:-> ]) == 0;
}
```

## comment_tweet function 

The `test comment_tweet` function validates the ability to comment on a tweet. It first retrieves an existing tweet from the `root` node with content `"test_like"`, then spawns the `comment_tweet` walker to add a comment with the content `"test_comment"`. The function checks if the comment's content matches the expected value, confirming that the comment was successfully added to the tweet.

Example:

```Jac
test comment_tweet {
    tweet = [root --> (`?Profile) --> (`?Tweet)](?content == "test_like")[0];
    tweet spawn comment_tweet(
        content = "test_comment",
    );
    comment = [tweet --> (`?Comment)][0];
    check comment.content == "test_comment";
}
```

## update comment function

The `test update_comment` function ensures that a comment on a tweet can be successfully updated. It retrieves an existing tweet with content `"test_like"` from the `root` node and accesses the associated comment. The function then spawns the `update_comment` walker to update the comment's content to `"new_comment"`. Finally, it verifies that the comment's content has been updated as expected, confirming that the update operation was successful.

Example:

```Jac
test update_comment{
    tweet = [root --> (`?Profile) --> (`?Tweet)](?content == "test_like")[0];
    comment = [tweet --> (`?Comment)][0];
    comment spawn update_comment(
        updated_content = "new_comment",
    );
    check comment.content == "new_comment";
}
```

## remove_comment function

The `test remove_comment` function verifies that a comment can be successfully removed from a tweet. It first retrieves an existing comment associated with a tweet from the `root` node. The function then spawns the `remove_comment` walker to remove the comment. Finally, it checks that no comments remain associated with the tweet, confirming that the removal was successful. 

Example:

```Jac
test remove_comment {
    comment = [root --> (`?Profile) --> (`?Tweet) --> (`?Comment)][0];
    comment spawn remove_comment();
    check len([root --> (`?Profile) --> (`?Tweet) --> (`?Comment)]) == 0;
}
```