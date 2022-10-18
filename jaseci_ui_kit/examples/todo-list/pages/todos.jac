import {*} with "../webkit/actions.jac";
import {*} with "../webkit/components.jac";
import {*} with "../webkit/edges.jac";


graph todo_list {
    ## this is necessary, but idk why
    has anchor root;

    spawn {
        root = spawn node::Container(name="mainContainer");
        header_text = spawn node::Text(variant="h1", value="Jaseci Todo-list", css={"textAlign": "center", "fontSize": "24px", "fontWeight": "bold", "marginBottom": "12px", "color": "#CA4316"});
        header_container = spawn node::Row(name="headerContainer", items="center", justify="center");
        task_list_container = spawn node::Container(name="taskListContainer", css={"background": "#EDEDEE", "height": "300px", "width": "480px", "overflowY": "auto", "borderRadius": "8px", "margin": "12px auto"});
        task_container = spawn node::Row(name="taskContainer", items="center", justify="start");
        inputBox = spawn node::Input(placeholder="Add a task");
        submitBtn = spawn node::Button(label="Add Task");

        add_todo_endpoint = spawn node::call_endpoint(
                                endpoint="http://localhost:8000/js/walker_run", 
                                method="POST", 
                                headers={
                                    'Authorization': "token 198ab01ffecda8b09c98e2e679257d25644c430690ae0cacd54529bcd83b0b9a",
                                    "Content-Type": "application/json"
                            });

        root -[section(name="children")]->header_text;
        root -[section(name="children")]-> header_container;
        root -[section(name="children")]-> task_list_container;
        
        header_container -[section(name="children")]-> inputBox;
        header_container -[section(name="children")]-> submitBtn;

        submitBtn-[event(trigger="onClick")]->add_todo_endpoint;
    }    
    
}