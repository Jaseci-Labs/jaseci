import React, { useState } from "react";
import './HelpPage.scss';
import { Tab, Nav, Row, Col, Container, Image } from 'react-bootstrap';
import exampleLabeled from './ExampleLLwithLabels.png';
import exampleSimple from './ExampleLL.png';
import exampleCreate from './Tutorial-CreateWorkette.png';
import exampleStarring from './Tutorial-CreateWorkette.png';


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
                                <img src={exampleSimple} alt="Example" class="img-thumbnail" />
                            </Tab.Pane>
                            <Tab.Pane eventKey="getting-started">
                                <h1>Getting Started</h1> 
                                    <h2>Building Your First Day</h2> 
                                        <img src={exampleCreate} alt="Example" class="img-thumbnail m-2" />
                                        <ol>
                                        <li>Setup a simple structure to organize your workettes (e.g. Personal, Work etc.)</li>
                                        <li>Create your workettes all the things you’d like to do</li>
                                        <li>Complete your workettes to log your accomplishments</li>
                                        </ol>
                                    <h2>Tips for Managing your Day</h2>
                                        <img src={exampleStarring} alt="Example" class="img-thumbnail m-2" />
                                        <ul>
                                            <li>Focus on the important things</li>
                                            <ul>
                                                <li>Early each day, review your workettes and click the star on the priority items</li>
                                                <li>You can also mark certain workettes as in progress</li>
                                            </ul>
                                            <li>Rank order priorities</li>
                                            <ul>
                                                <li>Click and drag to organize within work sets and workettes to rank prioritize what you want to do</li>
                                            </ul>
                                        </ul>
                            </Tab.Pane>
                            <Tab.Pane eventKey="day-view">
                                <h1>Day View</h1> 
                                <img src={exampleLabeled} alt="Example" class="img-thumbnail mb-3" />
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
                                <ol>
                                    <li>To move a work set or workette, click the folder icon and select where you would like to move</li>
                                </ol>
                                <h2>Rename workettes</h2>
                                <ol>
                                    <li>Click on the workette you’d like to rename</li>
                                    <li>Select the Gear icon</li>
                                    <li>Type in new name</li>
                                </ol>
                                <h2>Setup a Ritual</h2>
                                <ol>
                                    <li>Click on the Ritual icon for the workette you’d like to set up</li>
                                    <li>Click on the name of the workette to see the additional buttons</li>
                                    <li>Select the gear icon to open settings</li>
                                    <li>Select the days of the week you’d like to see this ritual (default is daily)</li>
                                </ol>
                                <h2>Permanently Delete a Workette</h2>
                                <ol>
                                    <li>Click on the Cancel button to abandon the workette</li>
                                    <li>Open the workette in the Abandoned section on the right column and then click on “Permanently Delete”</li>
                                </ol>
                            </Tab.Pane>
                            <Tab.Pane eventKey="reflect-view">
                                <h1>This Feature is Coming Soon!</h1>
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