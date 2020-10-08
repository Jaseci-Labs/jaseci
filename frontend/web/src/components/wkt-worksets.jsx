import React, { Component } from "react";
import WktItemList from "./wkt-item-list";
import { Container } from "react-bootstrap";

class WktWorksets extends Component {
  wkt_workset(w) {
    const ctx = w.context;
    const is_open = ctx.status === "open" || !ctx.status;
    if (ctx.wtype && ctx.wtype === "workset" && is_open) return true;
    return false;
  }

  render() {
    return (
      <Container fluid className="mr-0 pr-0">
        <WktItemList
          filter_func={this.wkt_workset}
          w_id={this.props.w_id}
          is_workset={true}
          color="#ffefcd"
        />
      </Container>
    );
  }
}

export default WktWorksets;
