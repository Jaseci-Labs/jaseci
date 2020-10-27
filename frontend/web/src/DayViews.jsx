import React, { Component } from "react";
import Day from "./components/day";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import { connect } from "react-redux";
import { session_actions as session } from "./store/session";
import { workette_actions as wact } from "./store/workette";
import DeepMITs from "./components/deep-mits";
import { Container } from "react-bootstrap";
import { time_now } from "./utils/utils";
import { workette_filters as w_filter } from "./utils/filters";

class DayViewLeft extends Component {
  state = { date: time_now() };

  componentDidMount() {
    this.onChange(time_now());
  }

  onChange = (date) => {
    const today = time_now();
    //if (date > today) date = today;
    this.props.change_date(date);
    const { workette } = this.props;
    const current = workette.days[date.toISOString().split("T")[0]];
    if (!current) {
      this.props.load_day(date.toISOString().split("T")[0]);
    }
    this.setState({ date });
  };

  render() {
    const { session, workette } = this.props;
    const { items } = workette;
    const current = workette.days[session.cur_date];

    return (
      <Container fluid className="m-0 p-0">
        <small>
          <Calendar value={this.state.date} onChange={this.onChange} />
        </small>
        <small>Ver. 0.39.2 </small>
        {current && (
          <DeepMITs
            w_id={current}
            label="Knock these out!"
            color="starred"
            items={w_filter.deepMIT()}
          />
        )}
        {current && (
          <DeepMITs
            w_id={current}
            label="Babysit these!"
            color="running"
            items={w_filter.deepRunning()}
          />
        )}
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

DayViewLeft = connect(map_state, left_map_dispatch)(DayViewLeft);

class DayViewRight extends Component {
  render() {
    const { session, workette } = this.props;
    const current = workette.days[session.cur_date];
    return (
      <Container fluid className="m-0 p-0">
        {current && (
          <DeepMITs
            w_id={current}
            label="Everything Completed!"
            color="mit-completed"
            items={w_filter.deepCompleted()}
          />
        )}

        {current && (
          <DeepMITs
            w_id={current}
            label="Everything Abandoned!"
            color="mit-abandoned"
            items={w_filter.deepCanceled()}
          />
        )}
      </Container>
    );
  }
}

DayViewRight = connect(map_state)(DayViewRight);

class DayViewMain extends Component {
  state = {};
  render() {
    const { session, workette } = this.props;
    return (
      <React.Fragment>
        {workette.days[session.cur_date] && <Day />}
      </React.Fragment>
    );
  }
}

DayViewMain = connect(map_state)(DayViewMain);

export { DayViewLeft, DayViewRight, DayViewMain };
