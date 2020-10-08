import React, { Component } from "react";
import WktItemSet from "./wkt-item-set";
import WktNotes from "./wkt-note-set";
import WktLinks from "./wkt-link-set";
import WktWorksets from "./wkt-worksets";
import WktAddForm from "./wkt-add";
import WktNoteForm from "./wkt-note";
import WktItemSingleForm from "./wkt-item-single-form";
import WktItemMoveForm from "./wkt-item-move-form";
import { is_today } from "../utils/utils";
import WktButton from "./wkt-button";
import {
  faPlusSquare,
  faEdit,
  faStickyNote,
  faEye,
  faLink,
  faBoxOpen,
} from "@fortawesome/free-solid-svg-icons";

import { Collapse, Container } from "react-bootstrap";
import { connect } from "react-redux";
import { workette_actions as wact } from "../store/workette";

class Workette extends Component {
  state = {
    show_add: false,
    show_edit: false,
    show_move: false,
    show_note: false,
    open_only: true,
  };

  componentDidMount() {
    const { items } = this.props.workette;
    const current = this.props.w_id;
    const item = items[current];
    if (item.context.note !== "" && item.context.wtype !== "workset")
      this.setState({ show_note: true });
  }

  update_workette = (ctx) => {
    const item = this.props.workette.items[this.props.w_id];
    if (!is_today(this.props.session.cur_date)) return;
    this.props.set_workette(item.jid, ctx);
  };

  delete_workette = () => {
    const item = this.props.workette.items[this.props.w_id];
    if (!is_today(this.props.session.cur_date)) return;
    this.props.delete_workette(item.jid, item.parent);
  };

  render() {
    const { session, workette } = this.props;
    const { items } = this.props.workette;
    const current = this.props.w_id;
    if (!items[current]) {
      return <div>Does not exist</div>;
    }
    return (
      <React.Fragment>
        <Container
          fluid
          className="border m-0 p-0"
          style={{ backgroundImage: "linear-gradient(#fffff5, #eeffff)" }}
        >
          <span>
            {/* <strong>
              {items[current].context.name && items[current].context.name}
            </strong> */}
            <WktButton
              icon={faPlusSquare}
              status={this.state.show_add}
              onClick={() => {
                this.setState({ show_add: !this.state.show_add });
              }}
            />
            {items[current].context.name && (
              <React.Fragment>
                <WktButton
                  icon={faEdit}
                  status={this.state.show_edit}
                  onClick={() => {
                    this.setState({ show_edit: !this.state.show_edit });
                  }}
                />
                <WktButton
                  icon={faBoxOpen}
                  status={this.state.show_move}
                  onClick={() => {
                    this.setState({ show_move: !this.state.show_move });
                  }}
                />
              </React.Fragment>
            )}
            <WktButton
              icon={faStickyNote}
              status={this.state.show_note}
              onClick={() => {
                this.setState({ show_note: !this.state.show_note });
              }}
            />
            <WktButton
              icon={faEye}
              status={!this.state.open_only}
              onClick={() => {
                this.setState({ open_only: !this.state.open_only });
              }}
            />
          </span>
          <Collapse in={this.state.show_add} unmountOnExit={true}>
            <div>
              <WktAddForm w_id={this.props.w_id} />
            </div>
          </Collapse>
          <Collapse in={this.state.show_edit} unmountOnExit={true}>
            <div>
              <WktItemSingleForm
                item={items[current]}
                update_func={this.update_workette}
                delete_func={this.delete_workette}
              />
            </div>
          </Collapse>
          <Collapse in={this.state.show_move} unmountOnExit={true}>
            <div>
              <WktItemMoveForm
                item={current}
                items={items}
                day={workette.days[session.cur_date]}
              />
            </div>
          </Collapse>
          <WktItemSet w_id={this.props.w_id} open_only={this.state.open_only} />
          <Collapse
            in={this.state.show_note || items[current].context.wtype === "note"}
            unmountOnExit={true}
          >
            <div>
              <WktNoteForm w_id={current} />
            </div>
          </Collapse>
          <WktLinks w_id={this.props.w_id} />
          <WktNotes w_id={this.props.w_id} />
          <WktWorksets w_id={this.props.w_id} />
        </Container>
      </React.Fragment>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
  api: state.api,
});

const map_dispatch = (dispatch) => ({
  set_workette: (w_id, ctx) => dispatch(wact.set_workette(w_id, ctx)),
  delete_workette: (w_id, parent_id) =>
    dispatch(wact.delete_workette(w_id, parent_id)),
});

export default connect(map_state, map_dispatch)(Workette);
