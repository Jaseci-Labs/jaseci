import React, { useState } from "react";
import './SplashPage.scss';
import { Navbar, Nav, Form, Button, Image } from "react-bootstrap";
import Countdown from 'react-countdown';
import logo from './transparent_white_logo.png';

const SplashPage = () => {
    const [showAccessCode, setShowAccessCode] = React.useState(false)
    const showAccessCodeForm = () => {
        setShowAccessCode(true);
    }

    //countdown
    // Renderer callback with condition
    const renderer = ({ days, hours, minutes, seconds, completed }) => {
        if (completed) {
            // Render a completed state
            return (
                <div className="--landing-countdown">
                    <span className="--landing-days">00</span>
                    <span className="--landing-hours">00</span>
                    <span className="--landing-minutes">00</span>
                    <span className="--landing-seconds">00</span>
                </div>
            );
        } else {
            // Render a countdown
            return (
                <div className="--landing-countdown">
                    <span className="--landing-days">{days}</span>
                    <span className="--landing-hours">{hours}</span>
                    <span className="--landing-minutes">{minutes}</span>
                    <span className="--landing-seconds">{seconds}</span>
                </div>
            );
        }
    };

    return (
        <>
            <div className="--landing-background">
                <Navbar>
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ml-auto">
                            <Nav.Link href="/login">Sign In</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
                <div className="--landing-main-content">
                    <Image src={logo} alt="LifeLogify Logo" fluid className="logo-img" />
                    <div className="logo-header">LifeLogify</div>
                    <h1 className="--landing-main-header">Growth via Intelligent Reflection</h1>
                    <h2 className="--landing-secondary-header">Coming soon, sign up below to get on the mailing list!</h2>
                    <Form inline>
                        <Form.Label htmlFor="inlineFormEmail" srOnly>
                            Email
                        </Form.Label>
                        <Form.Control
                            className="mb-2 mr-sm-2"
                            id="inlineFormEmail"
                            placeholder="Enter Email"
                        />
                        <Button type="submit" className="--landing-button mb-2">
                            Sign Up
                        </Button>
                    </Form>
                    <div className="--landing-access-code">
                        Already Have an Access Code? <a className="--landing-click-link" onClick={showAccessCodeForm} >Click Here</a>
                    </div>
                    {showAccessCode ?
                        <Form inline className="--landing-access-code-form">
                            <Form.Label htmlFor="accessCode" srOnly>
                                Access Code
                            </Form.Label>
                            <Form.Control
                                className="mb-2 mr-sm-2"
                                id="accessCode"
                                placeholder="Enter Access Code"
                            />
                            <Button type="submit" className="--landing-button mb-2">
                                Submit
                            </Button>
                        </Form>
                        : null
                    }

                </div>
                <Countdown
                    date={"01/01/2021"}
                    renderer={renderer}
                    daysInHours={true}
                />

                <div className="background-mask"></div>
            </div>
        </>)

}

export default SplashPage;