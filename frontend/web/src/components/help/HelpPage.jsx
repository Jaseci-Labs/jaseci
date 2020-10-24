import React, { useState } from "react";
import './HelpPage.scss';
import { Tab, Nav, Row, Col, Container } from 'react-bootstrap';

const HelpPage = () => {

    return (
        <Container className="mt-3">
            <Tab.Container id="left-tabs-example" defaultActiveKey="first">
                <Row>
                    <Col sm={3}>
                        <Nav variant="pills" className="flex-column">
                            <Nav.Item>
                                <Nav.Link eventKey="first">Day</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="second">How To's</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="third">Reflect</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Col>
                    <Col sm={9}>
                        <Tab.Content>
                            <Tab.Pane eventKey="first">
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
                                <h1>UI Overview</h1>
                                <ul>
                                </ul>

                                <h1>Getting Started - Building Your First Day</h1>
                                <ol>
                                    <li>Setup a simple structure to organize your workettes (e.g. Personal, Work etc.)</li>
                                    <li>Create your workettes all the things you’d like to do</li>
                                    <li>Complete your workettes to log your accomplishments</li>
                                </ol>

                                <h1>Basic Terminology</h1>
                                <ul>
                                    <li>Focusing on the important things</li>
                                    <ul>
                                        <li>Early each day, review your workettes and click the star on the priority items</li>
                                        <li>You can also mark certain workettes as in progress</li>
                                    </ul>
                                    <li>Click and drag to organize within work sets and workettes to rank prioritize what you want to do</li>
                                </ul>
                            </Tab.Pane>
                            <Tab.Pane eventKey="second">
                                <h1>Re-organize work sets or workettes</h1>
                                <ol>
                                    <li>To move a work set or workette, click the folder icon and select where you would like to move</li>
                                </ol>
                                <h1>Rename workettes</h1>
                                <ol>
                                    <li>Click on the workette you’d like to rename</li>
                                    <li>Select the Gear icon</li>
                                    <li>Type in new name</li>
                                </ol>
                                <h1>Setup a Ritual</h1>
                                <ol>
                                    <li>Click on the Ritual icon for the workette you’d like to set up</li>
                                    <li>Click on the name of the workette to see the additional buttons</li>
                                    <li>Select the gear icon to open settings</li>
                                    <li>Select the days of the week you’d like to see this ritual (default is daily)</li>
                                </ol>
                                <h1>Permanently Delete a Workette</h1>
                                <ol>
                                    <li>Click on the Cancel button to abandon the workette</li>
                                    <li>Open the workette in the Abandoned section on the right column and then click on “Permanently Delete”</li>
                                </ol>
                            </Tab.Pane>
                            <Tab.Pane eventKey="third">
                                <h1>Selecting a Date Range</h1>
                                <ol>
                                    <li>Click on the dates to modify the date range</li>
                                </ol>
                            </Tab.Pane>
                        </Tab.Content>
                    </Col>
                </Row>
            </Tab.Container>
        </Container>)

}

export default HelpPage;