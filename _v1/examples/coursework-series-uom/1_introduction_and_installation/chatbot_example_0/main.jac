# import the graph,kb file and walker made earlier.
import {*} with "./graph.jac";
import {*} with "./ask.jac";
import {*} with "./kb.jac";


walker init {
    root {
        spawn here ++> node::faq_root;
        spawn here walker::ingest_faq(kb_file="cloud.json");
        while (true){
            spawn here walker::ask;
        }
    }
}
