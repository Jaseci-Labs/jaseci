import React, { Component } from "react";
import { Draggable } from "react-beautiful-dnd";
import { Container, Row, Col } from "react-bootstrap";
import { Collapse } from "react-bootstrap";
import ReactTooltip from 'react-tooltip'

import Workette from "./workette";
import { is_today, validURL } from "../utils/utils";
import WktButton from "./wkt-button";
import { connect } from "react-redux";
import { workette_actions as wact } from "../store/workette";
import { workette_filters as w_filter } from "../utils/filters";
import {
  faCheckSquare,
  faTimesCircle,
  faSync,
  faStar,
  faRunning,
} from "@fortawesome/free-solid-svg-icons";
import "x-frame-bypass";
import './wkt-item-single.scss'

class WktItemSingle extends Component {
  state = {
    self_expand: this.props.is_workset ? false : false,
  };

  toggle_MIT = (item) => {
    if (!is_today(this.props.session.cur_date)) return;
    const val = this.props.item.context.is_MIT;
    this.props.set_workette(item.jid, { is_MIT: !val });
  };

  toggle_ritual = (item) => {
    if (!is_today(this.props.session.cur_date)) return;
    const val = this.props.item.context.is_ritual
      ? false
      : [1, 1, 1, 1, 1, 1, 1]; //Bitmap for days of the week maps to getDay func
    this.props.set_workette(item.jid, { is_ritual: val });
  };

  toggle_canceled = (item) => {
    if (!is_today(this.props.session.cur_date)) return;
    let val = this.props.item.context.status;
    if (val === "canceled") val = "open";
    else val = "canceled";
    this.props.set_workette(item.jid, { status: val });
  };

  toggle_done = (item) => {
    //hide tooltips to fix bug
    ReactTooltip.hide();
    if (!is_today(this.props.session.cur_date)) return;
    let val = this.props.item.context.status;
    if (val === "done") val = "open";
    else val = "done";
    this.props.set_workette(item.jid, { status: val });
  };

  toggle_running = (item) => {
    if (!is_today(this.props.session.cur_date)) return;
    let val = this.props.item.context.status;
    if (val === "running") val = "open";
    else val = "running";
    this.props.set_workette(item.jid, { status: val });
  };

  render() {
    const { item } = this.props;
    let color = this.props.color ? this.props.color : "white";
    if (this.props.is_workset && w_filter.countDeepChildren(item) === 0)
      color = this.props.empty_color;

    const is_workette =
      item.context.wtype !== "workset" &&
      item.context.wtype !== "note" &&
      item.context.wtype !== "link";

    return (
      <Draggable draggableId={item.jid} index={this.props.index}>
        {(provided) => (
          <React.Fragment>
            <Container
              fluid
              {...provided.draggableProps}
              ref={provided.innerRef}
              className="border"
            >
              <Row
                className={`d-flex justify-content-between color-${color}`}
              >
                {(is_workette || this.props.is_workset) && (
                  <Col xs="auto" className="m-0 p-0">
                    <WktButton
                      icon={faCheckSquare}
                      status={item.context.status === "done"}
                      tooltip="Complete"
                      onClick={() => this.toggle_done(item)}
                    />
                  </Col>
                )}
                <Col className="m-0 p-0">
                  <div
                    className="d-inline-flex ml-1"
                    {...provided.dragHandleProps}
                    onClick={() => {
                      this.setState({
                        self_expand: !this.state.self_expand,
                      });
                    }}
                    style={{ cursor: "pointer" }}
                  >
                    {item.context.owner && (
                      <span>[{item.context.owner}]&nbsp;</span>
                    )}
                    {this.state.self_expand && (
                      <strong>{item.context.name}</strong>
                    )}
                    {!this.state.self_expand && item.context.name}
                    {item.context.date && (
                      <span style={{ color: "grey" }}>
                        <small>
                          <i>&nbsp;({item.context.date})</i>
                        </small>
                      </span>
                    )}
                  </div>
                </Col>

                <Col xs="auto" className="m-0 p-0">
                  <div className="badge badge-info" style={{ opacity: 0.5 }}>
                    {w_filter.countDeepChildren(item) > 0 && (
                      <div>
                        {w_filter.countDeepChildrenClosed(item)}/
                        {w_filter.countDeepChildren(item)}
                      </div>
                    )}
                  </div>

                  {is_workette && (
                    <React.Fragment>
                      <WktButton
                        icon={faStar}
                        status={item.context.is_MIT}
                        tooltip="Knock this Out"
                        onClick={() => this.toggle_MIT(item)}
                      />
                      <WktButton
                        icon={faRunning}
                        status={item.context.status === "running"}
                        tooltip="In Progress"
                        onClick={() => this.toggle_running(item)}
                      />
                      <WktButton
                        icon={faSync}
                        status={item.context.is_ritual}
                        tooltip="Make Ritual"
                        onClick={() => {
                          this.toggle_ritual(item);
                          //this.setState({ self_expand: true });
                        }}
                      />
                    </React.Fragment>
                  )}
                  <WktButton
                    icon={faTimesCircle}
                    status={item.context.status === "canceled"}
                    tooltip="Cancel"
                    onClick={() => this.toggle_canceled(item)}
                  />
                  <div
                    {...provided.dragHandleProps}
                    className="d-inline-flex"
                  ></div>
                </Col>
              </Row>
            </Container>
            <Collapse in={this.state.self_expand} unmountOnExit={true}>
              <div>
                <div>
                  <Workette w_id={item.jid} />
                </div>
                {item.context.wtype === "link" && (
                  <div>
                    <a href={item.context.note} target="_blank">
                      Pop out to tab
                    </a>
                    {validURL(item.context.note) && (
                      <iframe
                        src={item.context.note}
                        style={{
                          width: "100%",
                          height: "800px",
                          maxHeight: "80vh",
                        }}
                      />
                    )}
                  </div>
                )}
              </div>
            </Collapse>
            {this.props.is_workset &&
              w_filter.countDeepChildren(item) !== 0 && <br />}
          </React.Fragment>
        )}
      </Draggable>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  workette: state.workette,
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  set_workette: (w_id, ctx) => dispatch(wact.set_workette(w_id, ctx)),
});

export default connect(map_state, map_dispatch)(WktItemSingle);
