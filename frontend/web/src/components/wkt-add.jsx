import React, { Component } from "react";
import { Input, Select, is_today, wtype_options } from "../utils/utils";
import { connect } from "react-redux";
import { workette_actions as wact } from "../store/workette";
import { Container, Row, Col } from "react-bootstrap";

class WktAddForm extends Component {
  state = { title: "", wtype: "" };

  componentDidUpdate(prevProps) {
    if (this.props.w_id !== prevProps.w_id) {
      this.setState({ title: "", wtype: "" });
    }
  }

  handleSubmit = (e) => {
    const current = this.props.w_id;
    e.preventDefault();
    if (is_today(this.props.session.cur_date))
      //Call Server
      this.props.create(current, this.state);
    this.setState({ title: "" });
  };

  handleChange = (e) => {
    if (e.currentTarget.name === "add") {
      this.setState({ title: e.currentTarget.value });
    } else if (e.currentTarget.name === "wtype") {
      this.setState({ wtype: e.currentTarget.value });
    }
  };

  render() {
    const { title, wtype } = this.state;
    return (
      <Container fluid>
        <form onSubmit={this.handleSubmit}>
          <Row>
            <Col className="col-md-auto pr-0 mr-0 ">
              <Select
                value={wtype}
                onChange={this.handleChange}
                name="wtype"
                options={wtype_options}
                extra_class="form-control-sm"
                description="Type"
              />
            </Col>
            <Col className="col pl-1 ml-1">
              <Input
                value={title}
                onChange={this.handleChange}
                name="add"
                extra_class="form-control-sm"
                description="Add a new workette. Press enter to add."
              />
            </Col>
          </Row>
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
  create: (w_id, title) => dispatch(wact.create_workette(w_id, title)),
});

export default connect(map_state, map_dispatch)(WktAddForm);
