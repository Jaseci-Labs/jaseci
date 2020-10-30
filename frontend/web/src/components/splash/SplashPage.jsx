import React, { useState } from "react";
import './SplashPage.scss';
import { Navbar, Nav, Form, Button, Image } from "react-bootstrap";
import Countdown from 'react-countdown';
import logo from './transparent_white_logo.png';
import Register from '../register'

const SplashPage = () => {
    // const [showAccessCode, setShowAccessCode] = React.useState(false)
    // const showAccessCodeForm = () => {
    //     setShowAccessCode(true);
    // }
    const [showRegister, setShowRegister] = useState(false)
    const showRegisterForm = () => {
        setShowRegister(true);
    }

    // //countdown
    // // Renderer callback with condition
    // const renderer = ({ days, hours, minutes, seconds, completed }) => {
    //     if (completed) {
    //         // Render a completed state
    //         return (
    //             <div className="--landing-countdown">
    //                 <span className="--landing-days">00</span>
    //                 <span className="--landing-hours">00</span>
    //                 <span className="--landing-minutes">00</span>
    //                 <span className="--landing-seconds">00</span>
    //             </div>
    //         );
    //     } else {
    //         // Render a countdown
    //         return (
    //             <div className="--landing-countdown">
    //                 <span className="--landing-days">{days}</span>
    //                 <span className="--landing-hours">{hours}</span>
    //                 <span className="--landing-minutes">{minutes}</span>
    //                 <span className="--landing-seconds">{seconds}</span>
    //             </div>
    //         );
    //     }
    // };

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
                    <Image src={logo} alt="LifeLogify Logo" fluid className="logo-img mb-3" />
                    {/* <div className="logo-header">LifeLogify</div> */}
                    <h1 className="--landing-main-header">A Revolutionary Way to Grow Yourself</h1>
                    <h2 className="--landing-secondary-header">Embark on your journey to a more powerful self</h2>
                    <Form>
                        {/* <Form.Group className="form-group" controlId="formGroupEmail">
                            <Form.Label htmlFor="inlineFormEmail" srOnly>
                                Email
                            </Form.Label>
                            <Form.Control
                                required
                                className="mr-sm-2"
                                id="inlineFormEmail"
                                placeholder="Enter Email"
                            />
                        </Form.Group> */}
                        
                        {/* {showRegister ?                            
                             <Form.Group className="form-group" controlId="formGroupName">
                                <Form.Label htmlFor="inlineFormName" srOnly>
                                    Name
                                </Form.Label>
                                <Form.Control
                                    className="mb-2 mr-sm-2"
                                    id="inlineFormName"
                                    placeholder="Enter Name"
                                />
                                <Form.Label htmlFor="inlineFormPassword" srOnly>
                                    Password
                                </Form.Label>
                                <Form.Control
                                    className="mb-2 mr-sm-2"
                                    id="inlineFormPassword"
                                    placeholder="Enter Password"
                                />
                                <Form.Label htmlFor="inlineFormPassword" srOnly>
                                    Re-enter Password
                                </Form.Label>
                                <Form.Control
                                    className="mb-2 mr-sm-2"
                                    id="inlineFormRePassword"
                                    placeholder="Re-enter Password"
                                />
                                <Form.Label htmlFor="inlineFormPassword" srOnly>
                                    Access Code
                                </Form.Label>
                                <Form.Control
                                    className="mb-2 mr-sm-2"
                                    id="inlineFormAccessCode"
                                    placeholder="Enter Access Code"
                                />
                            </Form.Group>
                            
                            : null
                        } */}
                        <div className="pt-2 d-flex justify-content-center">
                            {!showRegister ?                            
                                <Button type="button" className="--landing-button" onClick={showRegisterForm}>
                                    Get Started
                                </Button>
                                :
                                null
                            }
                        </div>
                        {showRegister ? <Register /> : null}
                    </Form>
                    {/* <div className="--landing-access-code">
                        Already Have an Access Code? <a className="--landing-click-link" href="/register" >Click Here</a>
                    </div> */}
                    {/* {showAccessCode ?
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
                    } */}

                </div>
                {/* <Countdown
                    date={"01/01/2021"}
                    renderer={renderer}
                    daysInHours={true}
                /> */}

                <div className="background-mask"></div>
            </div>
        </>)

}

export default SplashPage;