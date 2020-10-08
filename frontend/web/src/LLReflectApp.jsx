import React, { Component } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { DayViewLeft, DayViewRight, DayViewMain } from "./DayViews";
import { connect } from "react-redux";
import { session_actions as session } from "./store/session";
import axios from "axios";

class LLReflectApp extends Component {
  componentDidMount() {
    if (!this.props.session.logged_in) this.props.history.push("/login");
    else {
      axios.defaults.headers.common["Authorization"] =
        "token " + this.props.session.token;

      if (!this.props.session.jac_loaded) this.props.load_jac();
    }
  }

  render() {
    return (
      <Container fluid>
        {this.props.session.jac_loaded && (
          <Row style={{ height: "92vh" }}>
            <Col
              style={{
                minWidth: "350px",
                height: "100%",
                maxWidth: "400px",
                overflowY: "auto",
              }}
            >
              <Container>
                <DayViewLeft />
              </Container>
            </Col>
            <Col
              style={{
                minWidth: "400px",
                height: "100%",
                overflowY: "auto",
              }}
            >
              <DayViewMain />
            </Col>
            <Col
              style={{
                minWidth: "350px",
                height: "100%",
                maxWidth: "400px",
                overflowY: "auto",
              }}
            >
              <DayViewRight />
            </Col>
          </Row>
        )}
      </Container>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  load_jac: () =>
    axios.get("/ll.jac").then((r) => dispatch(session.load_jac(btoa(r.data)))),
});

export default connect(map_state, map_dispatch)(LLReflectApp);
