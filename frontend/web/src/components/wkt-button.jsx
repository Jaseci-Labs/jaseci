import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ToolTip from "react-portal-tooltip";

class WktButton extends Component {
  on_color = { color: "#000" };
  off_color = { color: "#00000040" };

  state = {
    isTooltipActive: false,
    delayHandler: null
  };

  showTooltip() {
    this.setState({
      delayHandler: setTimeout(() => {
        this.setState({ isTooltipActive: true });
      }, 400)
    })
  }
  hideTooltip() {
    clearTimeout(this.delayHandler)
    this.setState({ isTooltipActive: false });
  }

  render() {
    let style = {
      style: {
        background: 'white',
        padding: 5,
        boxShadow: '0 0 8px rgba(0,0,0,.3)',
        borderRadius: '3px',
        transition: `${this.state.transition} .1s ease-in-out, visibility .1s ease-in-out`,
        fontSize: '12px'
      },
      arrowStyle: {
        position: 'absolute',
        content: '""',
        transition: null
      }
    }
    return (
      <span
        ref={(element) => {
          this.element = element;
        }}
        className="mr-1"
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
            className="btn btn-success shadow border border-dark"
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
          tooltipTimeout="50"
          useHover={false}
          style={style}
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
