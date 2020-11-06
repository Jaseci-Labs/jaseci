import React, { Component } from "react";
import { Draggable } from "react-beautiful-dnd";
import { Container, Row, Col } from "react-bootstrap";
import { Collapse } from "react-bootstrap";

import Workette from "./workette";
import { check_frozen, validURL } from "../utils/utils";
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
  faLink,
  faStickyNote,
} from "@fortawesome/free-solid-svg-icons";
import "x-frame-bypass";
import { ReactTinyLink } from "react-tiny-link";
import "./wkt-item-single.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

class WktItemSingle extends Component {
  state = {
    self_expand: this.props.is_workset ? this.props.is_day : false,
  };

  toggle_MIT = (item) => {
    if (check_frozen(this.props.session)) return;
    const val = this.props.item.context.is_MIT;
    this.props.set_workette(item.jid, { is_MIT: !val });
  };

  toggle_ritual = (item) => {
    if (check_frozen(this.props.session)) return;
    const val = this.props.item.context.is_ritual
      ? false
      : [1, 1, 1, 1, 1, 1, 1]; //Bitmap for days of the week maps to getDay func
    this.props.set_workette(item.jid, { is_ritual: val });
  };

  toggle_canceled = (item) => {
    if (check_frozen(this.props.session)) return;
    let val = this.props.item.context.status;
    if (val === "canceled") val = "open";
    else val = "canceled";
    this.props.set_workette(item.jid, { status: val });
  };

  toggle_done = (item) => {
    if (check_frozen(this.props.session)) return;
    let val = this.props.item.context.status;
    if (val === "done") val = "open";
    else val = "done";
    this.props.set_workette(item.jid, { status: val });
  };

  toggle_running = (item) => {
    if (check_frozen(this.props.session)) return;
    let val = this.props.item.context.status;
    if (val === "running") val = "open";
    else val = "running";
    this.props.set_workette(item.jid, { status: val });
  };

  checkLinkTitle = (data) => {
    console.log(data);
    if (!this.props.item.context.name) {
      this.props.set_workette(this.props.item.jid, { name: data.title });
    }
  };

  render() {
    const { item } = this.props;
    let color = this.props.color ? this.props.color : "white";
    if (this.props.is_workset && w_filter.countDeepChildren(item) === 0)
      //If work set is empty, apply different color
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
              className="border-left border-bottom border-top border-light"
            >
              <Row className={`d-flex justify-content-between color-${color}`}>
                {(is_workette || item.context.wtype === "workset") && (
                  <Col xs="auto" className="m-0 p-0 pl-1">
                    <WktButton
                      icon={faCheckSquare}
                      status={item.context.status === "done"}
                      tooltip="Complete"
                      onClick={() => this.toggle_done(item)}
                    />
                  </Col>
                )}
                <Col className="d-flex align-items-center m-0 p-0">
                  <div
                    className="d-inline-flex ml-0"
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

                    {item.context.wtype === "link" && (
                      <Col
                        xs="auto"
                        className="m-0 p-0 pl-1 pr-1"
                        style={{ color: "gray" }}
                      >
                        <FontAwesomeIcon icon={faLink} />
                      </Col>
                    )}
                    {item.context.wtype === "note" && (
                      <Col
                        xs="auto"
                        className="m-0 p-0 pl-1 pr-1"
                        style={{ color: "gray" }}
                      >
                        <FontAwesomeIcon icon={faStickyNote} />
                      </Col>
                    )}

                    {this.state.self_expand && (
                      <strong>
                        {item.context.name.trim()
                          ? item.context.name
                          : "Untitled"}
                      </strong>
                    )}
                    {!this.state.self_expand &&
                      (item.context.name.trim()
                        ? item.context.name
                        : "Untitled")}
                    {item.context.date && (
                      <span style={{ color: "black" }}>
                        <small>
                          <i>&nbsp;({item.context.date})</i>
                        </small>
                      </span>
                    )}
                  </div>
                </Col>
                <Col xs="auto" className="d-flex align-items-center m-0 p-0">
                  <div
                    className="badge badge-info mr-1"
                    style={{
                      color: "black",
                      backgroundColor: "#00000015",
                      opacity: 1,
                    }}
                  >
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
                    {validURL(item.context.note) && (
                      <center>
                        <ReactTinyLink
                          cardSize="small"
                          showGraphic={true}
                          width="100%"
                          maxLine={2}
                          minLine={1}
                          url={item.context.note}
                          onSuccess={this.checkLinkTitle}
                        />
                        <iframe
                          is={
                            item.context.note.includes("docs.google.com")
                              ? ""
                              : "x-frame-bypass"
                          }
                          src={item.context.note}
                          style={{
                            width: "100%",
                            height: "800px",
                            maxHeight: "80vh",
                          }}
                        />
                      </center>
                    )}
                  </div>
                )}
              </div>
            </Collapse>
            {this.props.is_workset && <br />}
          </React.Fragment>
        )}
      </Draggable>
    ); // add w_filter.countDeepChildren(item) !== 0 && to get empty work set spacing
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
