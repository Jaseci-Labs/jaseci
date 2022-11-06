import {*} with "./actions.jac";
import {*} with "./components.jac";
import {*} with "./edges.jac";

graph my_site {
    ## this is necessary, but idk why
    has anchor root;

    spawn {
        root = spawn node::Container(name="mainContainer");
        hero = spawn node::Hero(name="hero1", background_image="https://i.imgur.com/0Z1Z0Zm.jpg");
        
        root-[section(name="children")]->hero;

        navbar1 = spawn root-[section(name="children")]->node::Navbar(
            name="navbar1", 
            links=[
                {"label": "Home", "href": "#"}, 
                {"label": "About", "href": "#"}
            ]
        );

       endpoint = spawn node::call_endpoint(
                                endpoint="http://localhost:8000/js/walker_run", 
                                method="POST", 
                                headers={
                                    'Authorization': "token 198ab01ffecda8b09c98e2e679257d25644c430690ae0cacd54529bcd83b0b9a",
                                    "Content-Type": "application/json"
                            });

        runOp = spawn node::run_operation(
                                operation="navbar1.sayHello", 
                                args=["a", "b"]
                            );

        navbar1-[event(trigger="onClick")]->endpoint;
        navbar1-[event(trigger="onClick")]->runOp;


        navbar1-[operation(name="op1", args=["a", "b"])]->spawn node::call_endpoint(
                                endpoint="http://localhost:8000/js/walker_run", 
                                method="POST", 
                                headers={
                                    'Authorization': "token 198ab01ffecda8b09c98e2e679257d25644c430690ae0cacd54529bcd83b0b9a",
                                    "Content-Type": "application/json"
                            });

s
        navbar1-[operation(name="op1")]->spawn node::show_toast(
                                message="Congratulations!", 
                                timeout=300
                            );


        // navbar1::on("click", );
        // navbar1.css.color = "red";
        // alert1 = spawn root-[section(name="right")]->node::Alert(name="alert1", message="Hello", palette="Primary");

        // alertBtn = spawn alert1-[section(name="children")]->node::Button(name="alertBtn", label="Click Me")
        //     -[section(name="children")]->node::Button(name="alertBtn1", label="Click Here");

        // alert1-[section(name="children")]->alertBtn;
        // alertBtn-[section(name="children")]->alertBtn2;
    }    
    
}


// An intelligent AI that integrates with slack to perform various company-related tasks.
// It receive some instruction, performs name entity extraction, to determine what tasks to perform and how to do it.
