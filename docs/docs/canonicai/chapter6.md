# Build a conversational AI system in Jaseci

# Chapter 6

## Bringing your application to production

### Register and update your jac code on a remote instance
In this section, we will walk you through on how to register and update your jac code on a remote instance. The steps are as follows:

#### Register jac code on a remote instance

First you have to login to jaseci control from the terminal.
```
jsctl -m
```

Then you will login into your remote instance by using the following. It will require you to pass in the username and password.
```
login [link here]
```

Terminal View
```
> Username: 
test
> Password:
password
```

Next step is to load all jaseci actions that the application requires. One of the earlier chapter we explained the ways of loading the actions and how to.
```
actions load remote [link to jaseci actions on remote]
```

We move on to registering the sentinel.
```
sentinel register -set_active true -mode ir [jir main file of the jaseci application]
```

After registering the sentinel we will have to create the graph for application and this goes as follows.
```
graph create -set_active true
```

If you have to delete the graph however, incase of a mistake you can do that using the following command and then you can recreate.
```
graph delete active:graph
```
Next step, you will have to run the init walker
```
walker run init
```

Great, and that's how you register jac code on a remote instance.

#### Updating jac code on a remote instance
Let us walk you through on how to update jac code on the remote instance. After you make your edits to the main jac file and build it. Run the following command each time you make an update to the jac code.

```
sentinel set -snt active:sentinel -mode ir [main jir file of the application]
```