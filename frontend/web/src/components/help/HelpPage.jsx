import React, { useState } from "react";
import './HelpPage.scss';
import { Tab, Nav, Row, Col, Container, Image } from 'react-bootstrap';

// overview images
import overview_example from './images/overview_example.png';

// getting started images
import gs_create from './images/gs_create.png';
import gs_leftview from './images/gs_leftview.png';
import gs_worksets from './images/gs_worksets.png';
import gs_workettes from './images/gs_workettes.png';
import gs_completing from './images/gs_completing.png';
 
// day images
import day_example from './images/day_example.png';
import day_move_workette from './images/day_move_workette.png';
import day_rename from './images/day_rename.png';
import day_ritual from './images/day_ritual.png';


const HelpPage = () => {

    return (
        <Container className="helppage pt-3" style={{ height: "100%", overflowY: "auto", overflowX:"hidden" }}>
            <Tab.Container id="left-tabs-example" defaultActiveKey="overview">
                <Row>
                    <Col sm={3}>
                        <Nav variant="pills" className="flex-column fixed-col">
                            <Nav.Item>
                                <Nav.Link eventKey="overview">Overview</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="getting-started">Getting Started</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="day-view">Day</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="reflect-view">Reflect</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Col>
                    <Col sm={9}>
                        <Tab.Content>
                            <Tab.Pane eventKey="overview">
                                <h1>UI Overview</h1>
                                <body>Welcome to LifeLogify! The Day view is what you will see upon logging in.  This is where you will be organizing and managing your days. At the top of the screen, you will see the navigation bar. This is how you can move to different parts of LifeLogify.</body> 
                                <br></br>
                                <img src={overview_example} alt="Example" class="img-thumbnail" />
                            </Tab.Pane>
                            <Tab.Pane eventKey="getting-started">
                                <h1>Getting Started</h1> 
                                    <h2>Understanding LifeLogify</h2>
                                    <ul>
                                        <li>LifeLogify is built to help realize the maximum potential of your productivity </li>
                                        <li>The Day page provides you an easy and efficient way to see what you need to do, prioritize those tasks, and track your accomplishments</li> 
                                        <li>As you track your activity, your past is recorded and frozen daily to preserve what you have done and allow for a history to be generated</li>
                                        <li>As your LifeLog builds up over time, you will be able to leverage other aspects of LifeLogify to optimize your days and plan for the future </li>
                                    </ul>
                                    <h2>Building Your First Day</h2> 
                                        <ol>
                                            <li>Setup a simple structure to organize your workettes in the way that makes the most sense to you. While you can move things around later, a good foundational structure will make it easy for you to find your tasks.</li>
                                            <img src={gs_worksets} alt="" class="img-thumbnail m2" />
                                            <li>Create your workettes all the things you’d like to do</li>
                                            <img src={gs_workettes} alt="" class="img-thumbnail m2" />
                                            <li>Complete your workettes to log your accomplishments</li>
                                            <img src={gs_completing} alt="" class="img-thumbnail m2" />
                                        </ol>
                                    <h2>Tips for Managing your Day</h2>
                                        <ul>
                                            <li>Focus on the important things</li>
                                            <ul>
                                                <li>Early each day, review your workettes and click the star on the priority items</li>
                                                <li>You can also mark certain workettes as in progress</li>
                                                <img src={gs_leftview} alt="Example" class="img-thumbnail m-2" />
                                            </ul>
                                            <li>Rank order priorities</li>
                                            <ul>
                                                <li>Click and drag to organize within work sets and workettes to rank prioritize what you want to do</li>
                                            </ul>
                                        </ul>
                            </Tab.Pane>
                            <Tab.Pane eventKey="day-view">
                                <h1>Day View</h1> 
                                <img src={day_example} alt="Example" class="img-thumbnail mb-3" />
                                <h1>Basic Terminology</h1>
                                <ul>
                                    <li><b>Workette - </b>Basic object used to represent a task</li>
                                    <ul>
                                        <li><b>Work Set - </b>A type of workette used to group smaller work sets and workettes</li>
                                        <li><b>Link - </b> A type of workette used to embed a link within your LifeLogify</li>
                                        <li><b>Note - </b> A type of workette used to store specific notes</li>
                                    </ul>
                                    <li><b>Ritual- </b>A recurring workette</li>
                                </ul>
                                
                                <h1>How To's</h1> 
                                <h2>Re-organize work sets or workettes</h2>
                                <img src={day_move_workette} alt="" class="img-thumbnail mb-3" />
                                <h2>Rename workettes</h2>
                                <img src={day_rename} alt="" class="img-thumbnail mb-3" />
                                <h2>Setup a Ritual</h2>
                                <img src={day_ritual} alt="" class="img-thumbnail mb-3" />
                                <h2>Permanently Delete a Workette</h2>
                                <ol>
                                    <li>Click on the Cancel button to abandon the workette</li>
                                    <li>Open the workette in the Abandoned section on the right column and then click on “Permanently Delete”</li>
                                </ol>
                            </Tab.Pane>
                            <Tab.Pane eventKey="reflect-view">
                                <h1>This section is still under construction and will be updated soon!</h1>
                                {/* <h1>Selecting a Date Range</h1>
                                <ol>
                                    <li>Click on the dates to modify the date range</li>
                                </ol> */}
                            </Tab.Pane>
                        </Tab.Content>
                    </Col>
                </Row>
            </Tab.Container>
        </Container>)

}

export default HelpPage;