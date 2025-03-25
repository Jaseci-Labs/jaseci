include jac_access_tag.jac;

obj Apple {
    has:priv num:int = 10;
}


with entry {
    print(jac_access_tag.num);
}