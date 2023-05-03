---
sidebar_position: 3
title: Playing with Walkers and Abilities
description: Purchasing and Selling items in Shop.
---

# Playing with Walkers and Abilities

## Checks the inventory

Walkers works as methods in traditional programming languages. Here is an example walker to get the current inventory of items in the shop.

```jac
walker inventory {
    has products = {};
    root: take --> node::product_catalog;
    product_catalog: take --> node::product;

    with exit {
        report products;
    }
}
```
- `has products = {}` This defines empty variable for products. This is a dictionary.
- `root: take --> node::product_catalog` This line says walker to traverse through `product_catalog` nodes.
- `product_catalog: take --> node::product` This line says walker to traverse through `product` nodes;
- `with exit {report products;}` This reports(returns) the return value from product nodes when exists from the product node.

To return the inventory from the product node we have to modify the product node which we already has in our jac program. 

```jac
node product {
    has name;
    has stock = 0;

    can check with inventory entry {
        visitor.products[here.name] = here.stock;
    }

}
```

-  ```
    can check with inventory entry {
        visitor.products[here.name] = here.stock;
    }
    ``` 
    this code snippet defines an ability of the product node. Which gives an ability to return current stock of the product node.
- `can check with inventory entry` This ability executes only when inventory walker enters into product node.
- `visitor.products[here.name] = here.stock;` Here the `here.name` represents the name of the current node and `here.stock` represents the stock of the current node. To get more context of the `here` keyword go to [here]. 

Copy the updated `product` node and the `inventory` walker into `shop.jac` program and execute it to see the following output.

Here we are running a specific walker. So use following command in the `jsctl` shell to run the `inventory` walker. 

```
jaseci > jac run shop.jac -walk inventory
```

The `walk` defines which walker to run. When we leave this parameter empty the `init` walker will run buy default. You can get more context on walkers [here](../../development/abstractions/walkers)

```json
{
  "success": true,
  "report": [
    {}
  ],
  "final_node": "urn:uuid:31c5607a-074c-4524-82bc-63dbc3d31b91",
  "yielded": false
}
```

- `report` represents the return value from the walker, but here you will see an empty dictionary as the output because we haven't add any stocks yet.

## Purchasing items

Now to add items into the stocks we have to purchase items. In this section we are going to add that part into our Jac program.

### Walker to Purchase items

To purchase items to stock we will define another walker named `purchase`;

```jac
walker purchase {
    has product_category, product_name, purchase_amount;
    root: take --> node::product_catalog;
    product_catalog {
        take -[category(name==product_category)]-> node::product(name==product_name) else {
            new_product = spawn node::product(name=product_name);
            here +[category(name=product_category)]+> new_product;
            take new_product;
            std.log("New product: " + product_name);
        }
    }
}
```

- `has product_category, product_name, purchase_amount` this line is defining 3 variables in `purchase` walker. These variables are `product_category`, `product_name` and `purchase_amount`.
- `root: take --> node::product_catalog` This line makes the walker to traverse the walker from root node to `product_catalog`.
- Rest of the code snippet is to add number of purchasing items if a product already exists. If not it will spawn a new product node from `product_category`.

### Node ability to increase the inventory with purchase

As of in the above example we will have to modify the `product` node to execute with the `purchase` walker entry.

```jac
node product {
    has name;
    has stock = 0;

    can check with inventory entry {
        visitor.products[here.name] = here.stock;
    }

    can stock_up with purchase entry {
        here.stock += visitor.purchase_amount;
        std.log("Stock for " + here.name + " up to " + (here.stock).str);
    }
}
```

- `here.stock += visitor.purchase_amount;` This will increase the stock by `purchase` amount. In this line `here` represents the current node while `visitor` represents the walker which is visiting the node at the moment.
- `std.log("Stock for " + here.name + " up to " + (here.stock).str);` This is a log statement. Logging in Jaseci can be done with `std.log`.

Now let's update the `shop.jac` program with above two code snippets and run the `shop.jac` with `` command. If everything is fine you'll see following output.

Now you can check the inventory again to see if the stock has been updated with the purchase operations.

## Sell products

Now lets see how to sell products using our `shop` application.  As in the above two examples here also we have to create a walker and a node ability to perform sell operations.

### Walker to sell a product to a customer

Let's understand the `sell` walker created to sell items.

```jac
walker sell {
    has product_category, product_name, sell_amount;
    root: take --> node::product_catalog;
    product_catalog {
        take -[category(name==product_category)]-> node::product(name==product_name) else {
            std.log("Sorry. We don't sell this product.");
        }
    }
}
```

- `has product_category, product_name, sell_amount;` This line defines 3 variable for `sell` walker named `product_category`, `product_name` and `sell_amount`.
- `root: take --> node::product_catalog;` This makes `sell` walker to traverse from root node to `product_catalog` node.
- Rest of the code snippet is to reduce the number of product items from `product_catalog` if the product is available and log a statement if product is not available. 

### Node ability to reduce inventory with item sell

As in above all examples here we have to add a node ability to the `product` node. Here is the updated node with `stock_down` node ability.

```jac
node product {
    has name;
    has stock = 0;

    can check with inventory entry {
        visitor.products[here.name] = here.stock;
    }

    can stock_up with purchase entry {
        here.stock += visitor.purchase_amount;
        std.log("Stock for " + here.name + " up to " + (here.stock).str);
    }

    can stock_down with sell entry {
        if(here.stock >= visitor.sell_amount) {
            here.stock -= visitor.sell_amount;
            std.log("Selling " + here.name + ": " + (visitor.sell_amount).str);
            std.log("Remaining stock: " + (here.stock).str);
        } else {
            std.log("Not enough stock for " + here.name);
        }
    }

}
```
`stock_down` node ability executes with `sell` walker entry. 

- `if(here.stock >= visitor.sell_amount)` this if statement execute if the current product stock is grater that the `sell_amount` of the `sell` walker visiting the product node.
 

```bash
jaseci> walker run sell -ctx "{\"product_category\": \"fruit\", \"product_name\": \"apple\", \"sell_amount\": 2"
```