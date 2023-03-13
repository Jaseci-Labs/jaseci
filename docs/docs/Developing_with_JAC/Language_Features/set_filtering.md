# **FILTERING REFERENCE USING SET OPERATION**

## **USE CASE**
- This is to simplify that kind of structure


### **[Current]**
```js
    root -> color(value=BLUE);
    root -> color(value=RED);
    root -> color(value=YELLOW);
    root -> color(value=GREEN);
    root -> color(value=ORANGE);
    root -> color(value=VIOLET);
    color(value=BLUE) -> color(value=GREEN);
    color(value=YELLOW) -> color(value=GREEN);
    color(value=RED) -> color(value=ORANGE);
    color(value=YELLOW) -> color(value=ORANGE);
    color(value=RED) -> color(value=VIOLET);
    color(value=BLUE) -> color(value=VIOLET);

    // mostly this will be the best structure for relational referencing
    // for example I need to find all colors comes from BLUE or can be created using BLUE
    // you just need to traverse starting on BLUE node
    // but this requires to create the relational tree ferencing so that you can traverse on any color

    // the syntax will look like this
    // for example I need to find all colors comes from BLUE or can be created using BLUE
    root {
        take --> node::color(value=BLUE);
    }

    color {
        take --> node::color;
        // just have a handling to stop repetition
    }
```
### **[New]**
```js
    // the simplified version will now look like this

    root -> color(value=BLUE, var=[blue]);
    root -> color(value=RED, var=[red]);
    root -> color(value=YELLOW, var=[yellow]);
    root -> color(value=GREEN, var=[blue,yellow]);
    root -> color(value=ORANGE, var=[red,yellow]);
    root -> color(value=VIOLET, var=[red,blue]);
    root -> color(value=LITE_VIOLET, var=[red,blue,white]);

    root {

        // I need to find all colors comes from BLUE or can be created using BLUE
        for color in --> node::color(var supersetof [blue]) {
            // BLUE GREEN VIOLET
        }

        // I need to find all colors that I can produce using sets of colors [red, blue, white]
        for color in --> node::color(var subsetof [red, blue, white]) {
            // VIOLET, LITE_VIOLET
        }

        // I need to find all colors that are not present(or made of) on the list [red, blue, white]
        for color in --> node::color(var disjointof [red, blue, white]) {
            // YELLOW
        }
    }
```