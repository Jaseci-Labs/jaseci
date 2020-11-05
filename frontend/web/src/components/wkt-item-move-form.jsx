import React, { Component } from "react";
import { check_frozen, MultiSelect, saveDelayTimeout } from "../utils/utils";
import { Container } from "react-bootstrap";
import { connect } from "react-redux";
import { workette_actions as wact } from "../store/workette";

class WktItemMoveForm extends Component {
  state = {
    timeout: null,
  };

  all_potential_parents = (item) => {
    const { items } = this.props;
    if (!(item in items)) return [];
    let ret = [];
    items[item].children.map((x) => {
      if (x !== this.props.item && items[x].context.name) {
        ret.push(...this.all_potential_parents(x));
      }
    });
    if (items[item].context.name) {
      ret.push(item);
    }
    return ret;
  };

  bread_crumb = (item) => {
    const { items } = this.props;
    let ret = "";

    //Day nodes do not have valid item ids so item ends up not having id
    if (!items[item] || items[item].context.day) return "";

    if (items[item].parent) ret += this.bread_crumb(items[item].parent);
    ret += "::" + items[item].context.name;
    return ret;
  };

  handleSubmit = (e) => {};

  handleChange = (e) => {
    if (
      e.currentTarget.name === "parent" &&
      !check_frozen(this.props.session)
    ) {
      if (window.confirm("Are you sure you want to move this item?")) {
        this.props.move_workette(this.props.item, e.currentTarget.value);
      }
    }
  };

  render() {
    const { new_parent } = this.state;
    const wtype_options = ["workette", "link", "note", "workset"];

    return (
      <Container fluid>
        <form onSubmit={this.handleSubmit}>
          <MultiSelect
            value={new_parent}
            onChange={this.handleChange}
            name="parent"
            options={[
              [this.props.day, "Top Level of Day"],
              ...this.all_potential_parents(this.props.day).map((x) => {
                return [x, this.bread_crumb(x)];
              }),
            ]}
            extra_class="form-control-sm"
            description="Enter new parent workette."
          />
        </form>
      </Container>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  workette: state.workette,
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  move_workette: (w_id, dest_node) =>
    dispatch(wact.move_workette(w_id, dest_node)),
});

export default connect(map_state, map_dispatch)(WktItemMoveForm);
