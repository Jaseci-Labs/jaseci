#version1
walker creator {
    can create with `<root> entry;
}

walker Travellor {
    can func_3 with `<root> entry;
}

node item {
    has val: int;

    can func_1 with creator | Travellor entry;
}

:node:item:can:func_1 {
    print("visiting ", <s>);
    if <s>.val == 2 and str(<h>) == 'Travellor()' {
        print("visiting again a specific node by w2\n");
    }
    visit --> else {
        print("finished visitng all nodes  ....\n");
    }
    ;
}

:walker:creator:can:create {
    end = <here>;
    for i=0 to i<5 by i+=1  {
        end ++> (end := item(val=i + 1));
    }
    visit -->;
}

:walker:Travellor:can:func_3 {
    visit(item(val=2));
}

with entry {
    <root> spawn creator();
    <r> spawn Travellor();
}
# #version2
# #1
# walker creator{
#      can create with `<root> entry;
# }

# node item{
#     has val :int;
#      can func_1 with creator entry;
# }

# :walker:creator:can:create{
#     end = <here>;
#     for i=0 to i<5 by i+=1 {
#         end ++>  end := item(val=i+1);
#     }

#             visit(item(val=2));
# }

# :node:item:can:func_1{
#         print("visiting ",<s>);
#  }

# with entry{
#          <root> spawn creator();
# }

# #2
# walker creator{
#      can create with `<root> entry;
# }

# node item{
#     has val :int;
#      can func_1 with creator entry;
# }

# :node:item:can:func_1{
#         print("visiting ",<s>);
#         visit-->else{
#                    print("finished visitng all nodes  ....\n");
#                  };
#  }

# :walker:creator:can:create{
#     end = <here>;
#     for i=0 to i<5 by i+=1 {
#         end ++>  end := item(val=i+1);
#     }

#     visit -->;
# }

# with entry{
#          <root> spawn creator();
# }
