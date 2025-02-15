import:py cache_pyast;
import:jac cache_jacast;

with entry{
    print(cache_jacast.add(1,2));
    print(cache_pyast.add(1,2));
}