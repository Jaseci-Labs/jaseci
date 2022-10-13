import {*} with "../webkit/actions.jac";
import {*} with "../webkit/components.jac";
import {*} with "../webkit/edges.jac";

graph todo_page {
    has anchor root;
    
    spawn {
        root = spawn node::Container(name="mainContainer");
        
    }
}