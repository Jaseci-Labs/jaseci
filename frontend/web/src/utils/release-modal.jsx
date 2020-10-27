import React, { Component, useState } from "react";
import { Modal, Button } from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import "./release-modal.scss";
import releaseNotes from "./release-notes.md";
import { workette_actions as wact } from "../store/workette";
import { connect } from "react-redux";
import { is_today } from "../utils/utils";

const LL_VER = process.env.REACT_APP_LL_VERSION;

class RNotes extends Component {
  state = { release_text: null };

  componentWillMount() {
    fetch(releaseNotes)
      .then((response) => response.text())
      .then((text) => {
        this.setState({ release_text: text.split("-----")[0] });
      });
  }

  render() {
    return (
      <div className="content">
        <ReactMarkdown source={this.state.release_text} />
      </div>
    );
  }
}

class ReleaseModal extends Component {
  state = { show: true };

  componentDidMount() {
    const { session, workette } = this.props;
    const current = workette.days[session.cur_date];
    const ll_ver = workette.items[current].context.ll_version;
    if (
      (ll_ver && ll_ver === LL_VER) ||
      !is_today(this.props.session.cur_date)
    ) {
      this.setState({ show: false });
    } else {
      this.props.set_workette(current, { ll_version: LL_VER });
    }
  }

  handleClose = () => this.setState({ show: false });
  handleShow = () => this.setState({ show: true });

  render() {
    return (
      <Modal
        centered
        show={this.state.show}
        onHide={this.handleClose}
        dialogClassName="release-modal"
      >
        <Modal.Header closeButton>
          <Modal.Title>New Features!</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <RNotes />
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={this.handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  workette: state.workette,
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  set_workette: (w_id, ctx) => dispatch(wact.set_workette(w_id, ctx)),
});

export default connect(map_state, map_dispatch)(ReleaseModal);
