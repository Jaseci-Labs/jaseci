# Global Vars
# Access Tags for Global Vars (public)
import:jac jac_access_tag_file1;

with entry {
    print(jac_access_tag_file1.num1);
}

# Access Tags for Global Vars (private)
with entry {
    print(jac_access_tag_file1.num2);
    # Cannot access 'num2', it is private to 'jac_access_tag_file1.jac'
}

# Enum
# Access Tags for Enum (public)
with entry{
    print(jac_access_tag_file1.Color.BLUE.value);
}

# Access Tags for Enum (private)
with entry{
    print(jac_access_tag_file1.Color.BLUE.value);
    # Not Allowed! Enum is private.
}

# Access Tags for Enum (protected)
with entry{
    print(jac_access_tag_file1.Color.BLUE.value);
}