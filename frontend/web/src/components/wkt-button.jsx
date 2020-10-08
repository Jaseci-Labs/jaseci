import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

class WktButton extends Component {
  on_color = { color: "#000" };
  off_color = { color: "#aaa" };
  render() {
    return (
      <span className="ml-1" onClick={this.props.onClick}>
        <FontAwesomeIcon
          icon={this.props.icon}
          style={this.props.status ? this.on_color : this.off_color}
        />
      </span>
    );
  }
}

export default WktButton;
