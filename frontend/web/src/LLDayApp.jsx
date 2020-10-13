import React, { Component } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { DayViewLeft, DayViewRight, DayViewMain } from "./DayViews";
import { connect } from "react-redux";
import { session_actions as session } from "./store/session";
import axios from "axios";
import WktButton from "./components/wkt-button";
import { faAlignCenter, faEye } from "@fortawesome/free-solid-svg-icons";

class LLDayApp extends Component {
  state = { show_left: true, show_right: true };
  componentDidMount() {
    if (!this.props.session.logged_in) this.props.history.push("/login");
    else {
      axios.defaults.headers.common["Authorization"] =
        "token " + this.props.session.token;

      if (!this.props.session.jac_loaded) this.props.load_jac();
    }
  }

  sidebar_style = (should_show) => {
    return {
      minWidth: should_show ? "300px" : "70px",
      maxHeight: "100%",
      maxWidth: should_show ? "350px" : "70px",
      overflowY: "auto",
    };
  };

  render() {
    return (
      <Container fluid style={{ height: "100%" }}>
        {this.props.session.jac_loaded && (
          <Row style={{ height: "100%", overflowY: "auto" }}>
            <Col
              style={this.sidebar_style(this.state.show_left)}
              className="border"
            >
              <Container>
                <center>
                  <WktButton
                    icon={faEye}
                    status={this.state.show_left}
                    onClick={() => {
                      this.setState({ show_left: !this.state.show_left });
                    }}
                  />
                </center>
                {this.state.show_left && <DayViewLeft />}
              </Container>
            </Col>
            <Col
              style={{
                minWidth: "400px",
                maxHeight: "100%",
                overflowY: "auto",
              }}
            >
              <DayViewMain />
            </Col>
            <Col
              style={this.sidebar_style(this.state.show_right)}
              className="border"
            >
              <center>
                <WktButton
                  icon={faEye}
                  status={this.state.show_right}
                  onClick={() => {
                    this.setState({ show_right: !this.state.show_right });
                  }}
                />
              </center>
              {this.state.show_right && <DayViewRight />}
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

export default connect(map_state, map_dispatch)(LLDayApp);
