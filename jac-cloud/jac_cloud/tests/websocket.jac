"""Websocket scenarios."""
import from jac_cloud.plugin {WEBSOCKET_MANAGER as socket}

###########################################################
#                   WEBSOCKET ENDPOINTS                   #
###########################################################

walker self_progress_notif {
    can enter1 with `root entry {
        socket.notify_self({"any_field": "for_progress", "progress": "0%", "status": "started"});
        report "do something 1";


        socket.notify_self({"any_field": "for_progress", "progress": "20%", "status": "inprogress"});
        report "do something 2";


        socket.notify_self({"any_field": "for_progress", "progress": "40%", "status": "inprogress"});
        report "do something 3";


        socket.notify_self({"any_field": "for_progress", "progress": "60%", "status": "inprogress"});
        report "do something 4";


        socket.notify_self({"any_field": "for_progress", "progress": "80%", "status": "inprogress"});
        report "do something 5";


        socket.notify_self({"any_field": "for_progress", "progress": "100%", "status": "completed"});
        report "do something 6";
    }

    class __specs__ {
        has methods: list = ["websocket"];
    }
}

walker user_progress_notif {
    has root_id: str;

    can enter1 with `root entry {
        _root = &(self.root_id);

        socket.notify_users([_root], {"any_field": "for_progress", "progress": "0%", "status": "started"});
        report "do something 1";


        socket.notify_users([_root], {"any_field": "for_progress", "progress": "20%", "status": "inprogress"});
        report "do something 2";


        socket.notify_users([_root], {"any_field": "for_progress", "progress": "40%", "status": "inprogress"});
        report "do something 3";


        socket.notify_users([_root], {"any_field": "for_progress", "progress": "60%", "status": "inprogress"});
        report "do something 4";


        socket.notify_users([_root], {"any_field": "for_progress", "progress": "80%", "status": "inprogress"});
        report "do something 5";


        socket.notify_users([_root], {"any_field": "for_progress", "progress": "100%", "status": "completed"});
        report "do something 6";
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}


walker channel_progress_notif {
    has channel_id: str;

    can enter1 with `root entry {
        socket.notify_channels([self.channel_id], {"any_field": "for_progress", "progress": "0%", "status": "started"});
        report "do something 1";


        socket.notify_channels([self.channel_id], {"any_field": "for_progress", "progress": "20%", "status": "inprogress"});
        report "do something 2";


        socket.notify_channels([self.channel_id], {"any_field": "for_progress", "progress": "40%", "status": "inprogress"});
        report "do something 3";


        socket.notify_channels([self.channel_id], {"any_field": "for_progress", "progress": "60%", "status": "inprogress"});
        report "do something 4";


        socket.notify_channels([self.channel_id], {"any_field": "for_progress", "progress": "80%", "status": "inprogress"});
        report "do something 5";


        socket.notify_channels([self.channel_id], {"any_field": "for_progress", "progress": "100%", "status": "completed"});
        report "do something 6";
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}

walker client_progress_notif {
    has client_id: str;

    can enter1 with `root entry {
        socket.notify_clients([self.client_id], {"any_field": "for_progress", "progress": "0%", "status": "started"});
        report "do something 1";


        socket.notify_clients([self.client_id], {"any_field": "for_progress", "progress": "20%", "status": "inprogress"});
        report "do something 2";


        socket.notify_clients([self.client_id], {"any_field": "for_progress", "progress": "40%", "status": "inprogress"});
        report "do something 3";


        socket.notify_clients([self.client_id], {"any_field": "for_progress", "progress": "60%", "status": "inprogress"});
        report "do something 4";


        socket.notify_clients([self.client_id], {"any_field": "for_progress", "progress": "80%", "status": "inprogress"});
        report "do something 5";


        socket.notify_clients([self.client_id], {"any_field": "for_progress", "progress": "100%", "status": "completed"});
        report "do something 6";
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}

walker something {
    can enter with `root entry {}

    class __specs__ {
        has auth: bool = False;
    }
}