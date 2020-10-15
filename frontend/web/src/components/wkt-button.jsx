import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ReactTooltip from 'react-tooltip';

class WktButton extends Component {
  on_color = { color: "#000" };
  off_color = { color: "#aaa" };
  render() {
    return (
      <span className="ml-1" onClick={this.props.onClick}>
        <FontAwesomeIcon
          icon={this.props.icon}
          data-tip={this.props.tooltip}
          style={this.props.status ? this.on_color : this.off_color}
        />
        <ReactTooltip place="top" type="dark" effect="float" />
      </span>
    );
  }
}

export default WktButton;
