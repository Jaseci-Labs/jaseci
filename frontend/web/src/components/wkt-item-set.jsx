import React, { Component } from "react";
import WktItemList from "./wkt-item-list";
import { Container, Row, Col } from "react-bootstrap";
import { connect } from "react-redux";
import { faSlash } from "@fortawesome/free-solid-svg-icons";
import { workette_filters as w_filter } from "../utils/filters";

class WktItemSet extends Component {
  render() {
    return (
      <Container fluid className="mr-0 pr-0">
        <Row>
          <Col style={{ minWidth: "300px" }}>
            <WktItemList filter_func={w_filter.open} w_id={this.props.w_id} />
            <WktItemList
              filter_func={w_filter.running}
              w_id={this.props.w_id}
              color="#ededff"
            />
          </Col>
          {!this.props.open_only && (
            <Col style={{ maxWidth: "36%", minWidth: "300px" }}>
              <WktItemList
                filter_func={w_filter.complete}
                w_id={this.props.w_id}
                color="#edffed"
              />

              <WktItemList
                filter_func={(w) => !w_filter.scheduled_now(w)}
                w_id={this.props.w_id}
                color="#ffffed"
              />
              <WktItemList
                filter_func={w_filter.canceled}
                w_id={this.props.w_id}
                color="#ffeeee"
              />
            </Col>
          )}
        </Row>
      </Container>
    );
  }
}

const map_state = (state) => ({
  session: state.session,
});

export default connect(map_state)(WktItemSet);
