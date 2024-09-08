node user_root {}

walker create_user {
    has user_info: dict = {};

    can spawn_user_root;
}

:walker:create_user:can:spawn_user_root {
    if self.user_info == {} {
        self.user_info = {
            "jid": "xxxx",
            "email": "yiping@myca.ai",
            "name": "Yiping Kang"
        };
    }
    visit [-->(`?user_root)](?jid == self.user_info["jid"]) else {
        n = here ++> user_root(
            jid=self.user_info["jid"],
            email=self.user_info["user"],
            name=self.user_info["name"]
        );
    }
}
