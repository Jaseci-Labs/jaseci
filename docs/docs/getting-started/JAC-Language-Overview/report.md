---
title: Grabbing Results from reports 
---

* It can be thought of as a global list that can be appended to by any walker throughout the request.
* The data returned from using the report is always a list.

```jac
node task{
    has anchor name, isCompleted;
}

walker myWalker{
    task{
        if(here.isCompleted){
            std.out('Completed');
        }else{
           std.out('not completed');
           report here;
        }
        take -->;

    }
}
```