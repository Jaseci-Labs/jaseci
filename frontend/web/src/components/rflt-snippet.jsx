import React, { Component } from "react";
import { connect } from "react-redux";
import { Container, Col } from "react-bootstrap";
import DeepMITs from "./deep-mits";
import { workette_filters as w_filter } from "../utils/filters";

class ReflectionSnippet extends Component {
  render() {
    const { session, workette } = this.props;
    const { items } = workette;
    const current = this.props.w_id;
    return (
      <Col
        className="col-3 mt-3"
        style={{
          minWidth: "400px",
          maxHeight: "50%",
          overflowY: "auto",
        }}
      >
        <Container fluid className="border rounded">
          <center>
            <strong>
              {new Date(items[current].context.day).toDateString()}
            </strong>
          </center>
          {current && (
            <DeepMITs
              w_id={current}
              label="Everything Completed!"
              color="#d4ffd4"
              items={w_filter.deepCompleted(current)}
            />
          )}
          {current && (
            <DeepMITs
              w_id={current}
              label="Everything Abandoned!"
              color="#ffdddd"
              items={w_filter.deepCanceled(current)}
            />
          )}
        </Container>
      </Col>
    );
  }
}

const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
});

export default connect(map_state)(ReflectionSnippet);
