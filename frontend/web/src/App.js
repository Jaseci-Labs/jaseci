import React from 'react';
import { Route, Switch } from 'react-router-dom';
import './App.css';
import './styles/colors.scss';
import { Provider } from "react-redux";
import store from "./store/store";
import NavBar from './components/navbar';
import LLReflectApp from './LLReflectApp';
import LLDayApp from './LLDayApp';
import { StatusBar } from './utils/utils'
import { LogIn, LogOut } from './components/login';
import Register from './components/register';
import { Container } from "react-bootstrap";

function App() {
    return (
        <Provider store={store}>
            <div>
                <NavBar style={{ height: "40px" }} />
                <Container fluid className="m-0 p-0" style={{ height: "calc(100vh - 70px)", backgroundColor: "#F8F8F8"}}>
                    <Switch>
                        <Route path="/login" component={LogIn} />
                        <Route path="/logout" component={LogOut} />
                        <Route path="/register" component={Register} />
                        <Route path="/reflect" component={LLReflectApp} />
                        <Route path="/" component={LLDayApp} />
                    </Switch>
                </Container>
                <StatusBar style={{ height: "30px" }} />
            </div>

        </Provider>
    );
}

export default App;
