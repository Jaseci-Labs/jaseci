edge married;
edge child;

node person {
    has id;
    has name;
    has date_of_birth;
    has profession;
    has gender;
    has deceased;
    has parents;
    has children;
    has spouse;
}
node family_root;

graph family_tree {
    has anchor family_root;
    spawn {
        family_root = spawn node::family_root;
    }
}