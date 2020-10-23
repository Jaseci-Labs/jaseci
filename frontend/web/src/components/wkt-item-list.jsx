import React, { Component } from "react";
import { DragDropContext, Droppable } from "react-beautiful-dnd";
import WktItemSingle from "./wkt-item-single";

import { workette_actions as wact } from "../store/workette";
import { is_today, move_arr_item } from "../utils/utils";
import { connect } from "react-redux";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { Container } from "react-bootstrap";

class WktItemList extends Component {
  state = { is_empty: true };

  handle_drag = (result) => {
    const { source, destination, draggableId } = result;
    const { items } = this.props.workette;
    const current = this.props.w_id;
    const { children } = items[current];
    if (
      !is_today(this.props.session.cur_date) ||
      !destination ||
      source.droppableId !== destination.droppableId ||
      source.index === destination.index
    )
      return;
    const src_idx = children.indexOf(draggableId);
    const dest_idx = children.indexOf(children[destination.index]);
    const new_order = move_arr_item(children, src_idx, dest_idx);
    this.props.set_workette(current, {
      order: new_order,
    });
  };

  showable = (item) => {
    const { is_empty } = this.state;
    if (!item.kind === "workette") return false;
    if (!this.props.filter_func(item)) return false;
    if (is_empty) this.setState({ is_empty: false });
    return true;
  };

  render() {
    const { items } = this.props.workette;
    const current = this.props.w_id;
    const { children } = items[current];

    return (
      <React.Fragment>
        <Container fluid className="m-0 p-0">
          <DragDropContext onDragEnd={this.handle_drag}>
            <Droppable droppableId={current}>
              {(provided) => (
                <div {...provided.droppableProps} ref={provided.innerRef}>
                  {children &&
                    children.map((i, idx) => (
                      <React.Fragment key={items[i].jid}>
                        {this.showable(items[i]) && (
                          <WktItemSingle
                            {...this.props}
                            item={items[i]}
                            index={idx}
                            is_workset={this.props.is_workset}
                          />
                        )}
                      </React.Fragment>
                    ))}

                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </DragDropContext>
          {!this.state.is_empty && !this.props.is_workset && <br />}
        </Container>
      </React.Fragment>
    );
  }
}

const map_state = (state) => ({
  workette: state.workette,
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  set_workette: (w_id, ctx) => dispatch(wact.set_workette(w_id, ctx)),
});

export default connect(map_state, map_dispatch)(WktItemList);
