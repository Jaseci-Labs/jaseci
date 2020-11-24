import React from 'react';
import { Route, Switch, withRouter } from 'react-router-dom';
import { TransitionGroup, CSSTransition } from "react-transition-group";
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

function App({ location }) {
    return (
        <div className="app-wrapper">
            <TransitionGroup className="transition-group">
                <CSSTransition
                    key={location.key}
                    timeout={{ enter: 700, exit: 700 }}
                    classNames={'fade'}
                >
                    <Provider store={store}>
                        <section className="route-section">
                            <Switch location={location}>
                                <InternalRoute path="/login" component={LogIn} />
                                <InternalRoute path="/logout" component={LogOut} />
                                <InternalRoute path="/register" component={Register} />
                                <InternalRoute path="/reflect" component={LLReflectApp} />
                                <InternalRoute path="/help" component={HelpPage} />
                                <InternalRoute path="/perform" component={LLDayApp} />
                                <Route path="/" component={SplashPage} />
                            </Switch>
                        </section>
                    </Provider>
                </CSSTransition>
            </TransitionGroup>
        </div>
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

export default withRouter(App);
