import React, { Component } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { ReflectViewLeft, ReflectViewMain } from "./ReflectViews";
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
      <Container fluid style={{ height: "100%" }}>
        {this.props.session.jac_loaded && (
          <Row style={{ height: "100%", overflowY: "auto" }}>
            <Col
              style={{
                minWidth: "300px",
                height: "100%",
                maxWidth: "350px",
                overflowY: "auto",
              }}
              className="border-right"
            >
              <Container>
                <ReflectViewLeft />
              </Container>
            </Col>
            <Col
              style={{
                minWidth: "400px",
                height: "100%",
                overflowY: "auto",
              }}
            >
              <ReflectViewMain />
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
