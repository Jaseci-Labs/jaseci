:walker:update_graph:can:go_to_user {
    visit [-->(?`user_root)](?jid==self.user_jid);
    visit [i for i in next if isinstance(i, day) and i.date == self.date];
}