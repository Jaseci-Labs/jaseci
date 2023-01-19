node simple { has value=null; }

walker here_fix_create {
  a=spawn here ++> node::simple;
  report a.info['jid'];
}

walker here_fix_update {
    here.context['value']="Test";
}

walker here_fix_check {
    take -->;
    simple {
       report here.context;
    }
}