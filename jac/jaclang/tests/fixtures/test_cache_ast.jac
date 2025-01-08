import:py test_cache_pyast;
import:jac test_cache_jacast;

with entry{
    print(test_cache_jacast.add(1,2));
    print(test_cache_pyast.add(1,2));
}