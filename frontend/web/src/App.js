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
import SplashPage from './components/splash/SplashPage'
import HelpPage from './components/help/HelpPage'
import { Container } from "react-bootstrap";

function App() {
    return (
        <Provider store={store}>
            <div>
                <Switch>
                    <InternalRoute path="/login" component={LogIn} />
                    <InternalRoute path="/logout" component={LogOut} />
                    <InternalRoute path="/register" component={Register} />
                    <InternalRoute path="/reflect" component={LLReflectApp} />
                    <InternalRoute path="/help" component={HelpPage} />\
                    <InternalRoute path="/day" component={LLDayApp} />
                    <Route path="/" component={SplashPage} />
                </Switch>
            </div>
        </Provider>
    );
}

const InternalRoute = ({ component: Component, ...rest }) => {
    return (
        <Route {...rest} render={props => (
            <div>
                <NavBar style={{ height: "40px" }} />
                <Container fluid className="m-0 p-0" style={{ height: "calc(100vh - 70px)", backgroundColor: "#FBFBFF" }}>
                    <Component {...props} />
                </Container>
                <StatusBar style={{ height: "30px" }} />
            </div>
        )
        } />
    )
}

export default App;
