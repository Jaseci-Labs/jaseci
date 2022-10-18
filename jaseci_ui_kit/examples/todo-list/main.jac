import {*} with "./walkers.jac";
import {*} with "./webkit/walkers.jac";
import {*} with "./pages/todos.jac";
node page;

walker init {
    root {
        todo_page = spawn here walker::create_page(page_graph=spawn graph::todo_list);
        json = spawn todo_page walker::pre_renderer;
        // ui_kit::register(graph="test", endpoint="/test");
    }
}