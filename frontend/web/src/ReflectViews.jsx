import React, { Component } from "react";
import Workette from "./components/workette";
import "react-calendar/dist/Calendar.css";
import { connect } from "react-redux";
import { session_actions as session } from "./store/session";
import { workette_actions as wact } from "./store/workette";
import { time_now, Input } from "./utils/utils";
import { Container, Row } from "react-bootstrap";
import ReflectionSnippet from "./components/rflt-snippet";

class ReflectViewLeft extends Component {
  state = {
    start_date: time_now().toISOString().split("T")[0],
    end_date: time_now().toISOString().split("T")[0],
  };

  getDaysInRange = (start, end) => {
    const ret = [];
    for (
      let r = new Date(start);
      r <= new Date(end);
      r.setDate(r.getDate() + 1)
    ) {
      ret.push(r.toISOString().split("T")[0]);
    }
    return ret;
  };

  handleChange = (e) => {
    let start = this.state.start_date;
    let end = this.state.end_date;
    if (e.currentTarget.name === "start_date") {
      start = e.currentTarget.value;
      this.setState({ start_date: start });
    } else if (e.currentTarget.name === "end_date") {
      end = e.currentTarget.value;
      this.setState({ end_date: end });
    }

    this.getDaysInRange(start, end).map((d) => {
      const { workette } = this.props;
      if (!workette.days[d]) {
        this.props.load_day(d);
      }
    });
  };

  render() {
    const { session, workette } = this.props;
    const { items } = workette;
    const current = workette.days[session.cur_date];
    const { start_date, end_date } = this.state;
    console.log(start_date);
    return (
      <Container fluid className="m-0 p-0">
        <Input
          value={start_date}
          max={end_date}
          type="date"
          onChange={this.handleChange}
          name="start_date"
          extra_class="form-control-sm"
          description="Enter date for workette."
        />
        <Input
          value={end_date}
          min={start_date}
          type="date"
          onChange={this.handleChange}
          name="end_date"
          extra_class="form-control-sm"
          description="Enter date for workette."
        />
      </Container>
    );
  }
}

const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
});

const left_map_dispatch = (dispatch) => ({
  change_date: (date) => dispatch(session.change_date(date)),
  load_day: (date) => dispatch(wact.load_day(date)),
});

ReflectViewLeft = connect(map_state, left_map_dispatch)(ReflectViewLeft);

class ReflectViewMain extends Component {
  state = {};

  allDayIds = () => {
    const { workette } = this.props;
    const ret = [];
    for (const d in workette.days) {
      ret.push(workette.days[d]);
    }
    return ret;
  };

  render() {
    const { session, workette } = this.props;
    return (
      <Container fluid>
        <Row style={{ height: "100%", overflowY: "auto" }}>
          {this.allDayIds().map((d_id) => (
            <ReflectionSnippet w_id={d_id} />
          ))}
        </Row>
      </Container>
    );
  }
}

ReflectViewMain = connect(map_state)(ReflectViewMain);

export { ReflectViewLeft, ReflectViewMain };
