import React, { Component } from "react";
import WktItemList from "./wkt-item-list";
import { Container } from "react-bootstrap";

class WktLinks extends Component {
  wkt_link(w) {
    const ctx = w.context;
    const is_open = ctx.status === "open" || !ctx.status;
    if (ctx.wtype && ctx.wtype === "link" && is_open) return true;
    return false;
  }

  render() {
    return (
      <Container fluid className="mr-0 pr-0">
        <WktItemList
          filter_func={this.wkt_link}
          w_id={this.props.w_id}
          color="#ededff"
        />
      </Container>
    );
  }
}

export default WktLinks;
