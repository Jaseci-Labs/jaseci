import React, { Component, useState } from "react";
import { Container, Row, Col, Modal, Button } from "react-bootstrap";
import ReactMarkdown from 'react-markdown';
import {render} from 'react-dom';
import RNotes from './release-notes';
import './release-modal.scss';


function ReleaseModal() {
    const [show, setShow] = useState(true);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    return (
        <Modal centered show={show} onHide={handleClose} dialogClassName="release-modal">
            <Modal.Header closeButton>
                <Modal.Title>New Features!</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <RNotes />
            </Modal.Body>

            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>Close</Button>
            </Modal.Footer>
        </Modal>  
    )

}

export default ReleaseModal