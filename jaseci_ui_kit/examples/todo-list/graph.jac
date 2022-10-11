import {*} with "./nodes.jac";
import {*} with "./walkers.jac";

graph app_graph {

    has anchor app;

    spawn {
        app = spawn node::app;
        
        tasks = spawn app --> node::tasks;
        pages = spawn app --> node::pages;

        homepage = spawn pages walker::create_page(name="homepage", path="/home");
        spawn homepage -[section(name="root")]-> graph::my_site;

        about = spawn pages walker::create_page(name="about", path="/about");
        spawn about -[section(name="root")]-> graph::about;
    }
}