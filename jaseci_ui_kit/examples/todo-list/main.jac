import {*} with "./walkers.jac";
import {*} with "./webkit/walkers.jac";
import {*} with "./graph.jac";
import {*} with "./site.jac";


walker init {
    root {
        // take --> node::app else { 
        spawn here --> graph::app_graph; 
        // }
    }
}