import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ToolTip from "react-portal-tooltip";

class WktButton extends Component {
  on_color = { color: "#000" };
  off_color = { color: "#00000040" };

  state = {
    isTooltipActive: false,
  };

  showTooltip() {
    this.setState({ isTooltipActive: true });
  }
  hideTooltip() {
    this.setState({ isTooltipActive: false });
  }

  render() {
    return (
      <span
        ref={(element) => {
          this.element = element;
        }}
        className="pr-1"
        onClick={this.props.onClick}
      >
        {this.props.icon && (
          <FontAwesomeIcon
            icon={this.props.icon}
            style={this.props.status ? this.on_color : this.off_color}
            onMouseEnter={this.showTooltip.bind(this)}
            onMouseLeave={this.hideTooltip.bind(this)}
          />
        )}
        {!this.props.icon && (
          <button
            className="btn btn-success"
            onMouseEnter={this.showTooltip.bind(this)}
            onMouseLeave={this.hideTooltip.bind(this)}
          >
            {this.props.label}
          </button>
        )}
        <ToolTip
          active={this.state.isTooltipActive}
          position="top"
          arrow="center"
          parent={this.element}
        >
          <div>
            <p className="m-0 p-0">{this.props.tooltip}</p>
          </div>
        </ToolTip>
      </span>
    );
  }
}

export default WktButton;
