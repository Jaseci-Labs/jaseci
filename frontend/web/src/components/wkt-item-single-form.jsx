import React, { Component } from "react";
import {
  Input,
  Select,
  CheckBox,
  saveDelayTimeout,
  wtype_options,
} from "../utils/utils";
import { Collapse, Container, Row, Col } from "react-bootstrap";

class WktItemSingleForm extends Component {
  state = {
    timeout: null,
    name: "",
    owner: "",
    wtype: "",
    snooze_till: "",
    is_ritual: false,
    last_written: null,
  };

  updateStateLinked = () => {
    const {
      name,
      owner,
      wtype,
      is_ritual,
      snooze_till,
      last_written,
    } = this.props.item.context;
    this.setState({
      name: name ? name : "",
      owner: owner ? owner : "",
      wtype: wtype ? wtype : "",
      snooze_till: snooze_till ? snooze_till : "",
      is_ritual: is_ritual ? is_ritual : false,
      last_written: last_written ? last_written : null,
    });
  };

  componentDidUpdate() {
    const { last_written } = this.props.item.context;
    if (last_written && last_written > this.state.last_written)
      this.updateStateLinked();
  }

  componentDidMount() {
    this.updateStateLinked();
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.props.update_func(this.state);
  };

  handleChange = (e) => {
    if (e.currentTarget.name === "name") {
      this.setState({ name: e.currentTarget.value });
    } else if (e.currentTarget.name === "owner") {
      this.setState({ owner: e.currentTarget.value });
    } else if (e.currentTarget.name === "wtype") {
      this.setState({ wtype: e.currentTarget.value });
    } else if (e.currentTarget.name === "snooze_till") {
      this.setState({ snooze_till: e.currentTarget.value });
    }
    this.setState({
      timeout: saveDelayTimeout(this.state.timeout, () => this.handleSubmit(e)),
    });
  };

  handleRitChange = (e) => {
    let { is_ritual } = this.state;
    //If ritual deactivated, reactivate
    if (!is_ritual) {
      is_ritual = [1, 1, 1, 1, 1, 1, 1];
    }
    switch (e.currentTarget.name) {
      case "mon":
        is_ritual[0] = !is_ritual[0];
        break;
      case "tues":
        is_ritual[1] = !is_ritual[1];
        break;
      case "wed":
        is_ritual[2] = !is_ritual[2];
        break;
      case "thurs":
        is_ritual[3] = !is_ritual[3];
        break;
      case "fri":
        is_ritual[4] = !is_ritual[4];
        break;
      case "sat":
        is_ritual[5] = !is_ritual[5];
        break;
      case "sun":
        is_ritual[6] = !is_ritual[6];
        break;
      default:
        break;
    }
    //If no day set for ritual turn ritual off
    if (!is_ritual.filter((i) => i).length) is_ritual = false;
    this.setState({ is_ritual: is_ritual });
    this.setState({
      timeout: saveDelayTimeout(this.state.timeout, () => this.handleSubmit(e)),
    });
  };

  handleDelete = (e) => {
    e.preventDefault();
    if (window.confirm("Are you sure?")) {
      this.props.delete_func();
    }
  };

  render() {
    const { name, owner, wtype, snooze_till } = this.state;
    let { is_ritual } = this.state;

    //Detected if ritual turned on elsewhere then set checkbox values
    const true_rit = this.props.item.context.is_ritual;
    if (true_rit && !is_ritual) {
      is_ritual = this.props.item.context.is_ritual;
    }

    return (
      <Container fluid>
        <form onSubmit={this.handleSubmit}>
          <Row>
            <Input
              value={name}
              onChange={this.handleChange}
              name="name"
              extra_class="form-control-sm"
              description="Enter title of workette."
            />
            &nbsp;&nbsp;
            <Select
              value={wtype}
              onChange={this.handleChange}
              name="wtype"
              options={wtype_options}
              extra_class="form-control-sm"
              description="Enter type of workette."
            />
          </Row>
          <Row>
            <Input
              value={owner}
              onChange={this.handleChange}
              name="owner"
              extra_class="form-control-sm"
              description="Enter workette owner."
            />
            &nbsp;&nbsp;
            <Input
              value={snooze_till}
              type="date"
              onChange={this.handleChange}
              name="snooze_till"
              extra_class="form-control-sm"
              description="Enter date for workette."
            />
          </Row>

          <Collapse in={this.props.item.context.is_ritual ? true : false}>
            <Row>
              <small>
                <div>Ritual recurs every</div>

                <CheckBox
                  value={is_ritual[0]}
                  onChange={this.handleRitChange}
                  name="mon"
                  label="Monday"
                />
                <CheckBox
                  value={is_ritual[1]}
                  onChange={this.handleRitChange}
                  name="tues"
                  label="Tuesday"
                />
                <CheckBox
                  value={is_ritual[2]}
                  onChange={this.handleRitChange}
                  name="wed"
                  label="Wednesday"
                />
                <CheckBox
                  value={is_ritual[3]}
                  onChange={this.handleRitChange}
                  name="thurs"
                  label="Thursday"
                />
                <CheckBox
                  value={is_ritual[4]}
                  onChange={this.handleRitChange}
                  name="fri"
                  label="Friday"
                />
                <CheckBox
                  value={is_ritual[5]}
                  onChange={this.handleRitChange}
                  name="sat"
                  label="Saturday"
                />
                <CheckBox
                  value={is_ritual[6]}
                  onChange={this.handleRitChange}
                  name="sun"
                  label="Sunday"
                />
              </small>
            </Row>
          </Collapse>
        </form>
        {this.props.item.context.status === "canceled" && (
          <center>
            <a href="#" onClick={this.handleDelete}>
              <small>Permanently Delete</small>
            </a>
          </center>
        )}
      </Container>
    );
  }
}

export default WktItemSingleForm;
