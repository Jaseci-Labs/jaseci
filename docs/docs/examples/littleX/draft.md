# Detailed Explanation on littleX test cases.

To write test cases for **littleX** , create a file with the extension `.test.jac`. This test file should be placed in the same context or directory as the Jac module or walker you intend to test to ensure proper access to the target elements. Within the `littleX.test.jac` file, you can define test functions using the `test` keyword, followed by a descriptive name (e.g., test create_tweet). Each test should simulate a scenario where a specific function or walker is invoked and its behavior is validated.

Use the `check` statement within the test body to assert the expected outcome of the logic under test. The `check` keyword performs an assertion and will cause the test to fail if the condition is not met. This helps ensure that your logic works as intended and guards against regressions. You can use expressions like `check obj.attr == expected_value`, `check len(collection) == expected_count`, or similar validations.

Tests can include operations like updating node attributes, verifying edge relationships, and checking object states before and after the action. The structure encourages clean and modular testing aligned with the Jac programming model.

Example test case:

```Jac
test create_profile {
    root spawn create_profile(             //spawn walker
        username = "JohnDoe",
    );
    profile = [root --> (`?Profile)][0];   // Retrieve the Profile node
    check isinstance(profile, Profile);    // Check if it is a Profile
    check profile.username == "JohnDoe";   // Verify the username
}
```

## visit_profile test case

The `visit_profile` functionality verifies whether a `Profile` node is connected to the `root` node. If such a node exists, it navigates to the connected profile; otherwise, it creates a new `Profile` node and proceeds to visit it. To test this behavior, the `visit_profile` walker should be spawned on the `root` node. After execution, the `Profile` node linked to the `root` can be retrieved and validated to confirm that it is indeed an instance of the `Profile` archetype.

spawn walker : ``root spawn visit_walker();``
filtering profile node: ``profile = [root --> (`?Profile)][0];``
check is this node Profile or not : ``check isinstance(profile,Profile);``

Complete test case:

```Jac
test visit_profile {
    root spawn visit_profile();
    profile = [root --> (`?Profile)][0];
    check isinstance(profile,Profile);
}
```
## update_profile test case

The `update_profile` walker is responsible for updating the username of a `Profile` node. It first checks whether a `Profile` node is connected to the `root`. If such a node exists, it visits it; otherwise, it creates a new `Profile` node and proceeds to update it.
To test this functionality, the `update_profile` walker should be spawned from the `root` node. After execution, the connected `Profile` node can be retrieved and verified to ensure that the username has been correctly updated.

spawn walker: ``root spawn update_profile();``
filter profile node : ``profile = [root --> (`?Profile)][0];``
check updated username : ``check profile.username == "test_user";``

Complete test case:

```Jac
test update_profile {
    root spawn update_profile(
        new_username = "test_user",
    );
    profile = [root --> (`?Profile)][0];
    check profile.username == "test_user";
}
```

## follow_request test case

The `test follow_request` ensures that a profile can successfully initiate a follow request to another profile using the `follow_request` walker. A new `Profile` node, named "Sam," is created to serve as the followee. After executing the walker, the test proceeds by navigating from the followee to confirm the presence of a Follow edge, which indicates the successful creation of the follow request. Finally, the test verifies that the username of the connected profile matches the expected followee.

create followee profile : ``followee = Profile("Sam");``
spawn walker : ``followee spawn follow_request();``
filter followee profile : ``followee_profile = [root --> (`?Profile)-:Follow:->(`?Profile)][0];``
check followee profile username : ``check followee_profile.username == "Sam";``

Completed test case:

```Jac
test follow_request {
    followee = Profile("Sam");
    followee spawn follow_request();
    followee_profile = [root --> (`?Profile)-:Follow:->(`?Profile)][0];
    check followee_profile.username == "Sam";
}
```

## un_follow_request test case

The `test un_follow_request` verifies that a follow relationship can be successfully removed between two profiles. It first checks whether there are any follow requests from the `follower profile` to the `followee profile`. To conduct the test for `un_follow_request`, the `un_follow_request` walker is first spawned on the `profile` node. The test ultimately examines how many follow connections remain, ensuring that the `un_follow_request` walker accurately handles the removal of follow edges in the graph.

filter profile node : ``followee = [root --> (`?Profile)-:Follow:->(`?Profile)][0];``
spawn walker : ``followee spawn un_follow_request();``
check length of the profiles that connect within Follow edge : ```check len([root --> (`?Profile)-:Follow:->(`?Profile)]) == 0;```

Complete test case:

```Jac
test un_follow_request {
    followee = [root --> (`?Profile)-:Follow:->(`?Profile)][0];
    followee spawn un_follow_request();
    check len([root --> (`?Profile)-:Follow:->(`?Profile)]) == 0;
}
```

## create tweet test case

The `test create_tweet` test verifies whether a tweet is created correctly. To perform this test, the `create tweet` walker is spawned on the root node. The test then checks whether there are any `tweet` nodes connected to the `profile` node. Finally, it validates that the tweet has been correctly created and linked as expected.

spawn walker : `root spawn create_tweet();`
filter tweet node : ``test1 = [root --> (`?Profile) --> (`?Tweet)][0];``
check tweet is correctly created : `check test1.content == "test_tweet";`

Complete test case:

```Jac
test create_tweet {
    root spawn create_tweet(
        content = "test_tweet",
    );
    test1 = [root --> (`?Profile) --> (`?Tweet)][0];
    check test1.content == "test_tweet";
}
```

## update_tweet test case

The `test update_tweet` verifies that the content of a tweet can be successfully updated. It begins by checking whether any `tweet` nodes are connected to a `Profile` node. If such a connection exists, the test proceeds to visit the associated node. To perform the update, the `update_tweet` walker is spawned on the `tweet_node`. Finally, the test checks whether the tweet's content has been correctly updated.

filter is there any tweets : ``tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];``
spawn walker : `tweet1 spawn update_tweet();`
check tweet is updated : `check tweet1.content == "new_tweet";`

Complete test case:

```Jac
test update_tweet {
    tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];
    tweet1 spawn update_tweet(
        updated_content = "new_tweet",
    );
    check tweet1.content == "new_tweet";
}
```

## Remove_tweet test case

The `test remove_tweet` test case verifies the successful deletion of a tweet. It begins by retrieving an existing tweet associated with the `tweet` node through traversal from the profile. Subsequently, the `remove_tweet` walker is spawned from the `tweet node` to initiate the removal process. Finally, the test confirms that no tweets remain linked to the profile, thereby validating that the tweet has been successfully deleted.

checks is there any tweets : ``tweet2 =  [root --> (`?Profile)--> (`?Tweet)][0];``
spawn walker : `tweet2 spawn remove_tweet();`
check tweet is removed : ``check len([root --> (`?Profile) --> (`?Tweet)]) == 0;``

Complete test case:

```Jac
test remove_tweet {
    tweet2 =  [root --> (`?Profile)--> (`?Tweet)][0];
    tweet2 spawn remove_tweet();
    check len([root --> (`?Profile) --> (`?Tweet)]) == 0;
}
```

## Like_tweet test case

The `test like_tweet` verifies the capability of a profile to like a tweet. It starts by creating a tweet from the `root` node and then navigates to the corresponding `tweet` node. The process continues by spawning the `like_tweet` walker from the `tweet1` node. Finally, it confirms that the username `"test_user"` is correctly associated with the `Like` relationship on the tweet.

spawn walker : `root spawn create_tweet(0);`
filter is there any tweets : ``tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];``
spawn walker : `tweet1 spawn like_tweet();`
filter is like to tweet : `test1 = [tweet1 -:Like:-> ][0];`
check liked profile username : ` check test1.username == "test_user";`

Complete test case:

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

## remove_like test case

The `test remove_like` checks the functionality of removing a like from a tweet. It first retrieves an existing tweet; if the tweet exists, it proceeds to visit the tweet node. Then, it spawns the `remove_like` walker from the `tweet` node. The function subsequently checks whether the `Like` relationship has been successfully removed by confirming that the length of the associated likes is zero.

check is there any liked tweets : ``tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];``
spawn walker : `tweet1 spawn remove_like();`
check like is removed : `check len([tweet1 -:Like:-> ]) == 0;`

Complete test case:

```Jac
test remove_like {
    tweet1 = [root --> (`?Profile) --> (`?Tweet)][0];
    tweet1 spawn remove_like();
    check len([tweet1 -:Like:-> ]) == 0;
}
```

## comment_tweet test case

The `test comment_tweet` verifies the ability to comment on a tweet. It begins by checking whether there is any tweet with content similar to `'test_like'`. If such a tweet exists, it proceeds to visit it. To test the `comment_tweet` functionality, the function spawns a `comment_tweet` node on the `tweet` node and filters the `comment` node connected to the tweet. Finally, it verifies whether the content of the comment matches the expected value, confirming that the comment was successfully added to the tweet.

filter tweet's content : ``tweet = [root --> (`?Profile) --> (`?Tweet)](?content == "test_like")[0];``
spawn walker : `tweet spawn comment_tweet();`
filter commnet : ``comment = [tweet --> (`?Comment)][0];``
check comment correctly added or not : `check comment.content == "test_comment";`

Complete test case:

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

## update comment test case

The `test update_comment` verifies that a comment on a tweet can be successfully updated. It begins by retrieving an existing tweet with the content `"test_like"` and accesses its associated comment. Then, the `update_comment` walker is spawned on the `comment` node to perform the update operation. Finally, the test checks whether the comment has been updated correctly.

filter tweet's content : ``tweet = [root --> (`?Profile) --> (`?Tweet)](?content == "test_like")[0];``
filter comment : ``comment = [tweet --> (`?Comment)][0];``
spawn walker : `comment spawn update_comment();`
check comment is updated or not : `check comment.content == "new_comment";`

Complete test case:

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

## remove_comment test case

The `test_remove_comment` verifies that a comment can be successfully removed from a tweet. It begins by retrieving an existing comment associated with a tweet from the `tweet` node. To test the `remove_comment` functionality, the `remove_comment` walker is spawned on the `comment` node to remove the comment. Finally, the test checks that no comments remain associated with the tweet, confirming that the removal was successful.

filter is there any comment : ``comment = [root --> (`?Profile) --> (`?Tweet) --> (`?Comment)][0];``
spawn walker : `comment spawn remove_comment();`
check comment successfully removed : ``check len([root --> (`?Profile) --> (`?Tweet) --> (`?Comment)]) == 0;``

Complete test case:

```Jac
test remove_comment {
    comment = [root --> (`?Profile) --> (`?Tweet) --> (`?Comment)][0];
    comment spawn remove_comment();
    check len([root --> (`?Profile) --> (`?Tweet) --> (`?Comment)]) == 0;
}
```