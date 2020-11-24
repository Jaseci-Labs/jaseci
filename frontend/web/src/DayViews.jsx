import React, { Component } from "react";
import Day from "./components/day";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./DayViews.scss";
import { connect } from "react-redux";
import { session_actions as session } from "./store/session";
import { workette_actions as wact } from "./store/workette";
import WktNoteForm from "./components/wkt-note";
import DeepMITs from "./components/deep-mits";
import { Container, Row, Col } from "react-bootstrap";
import WktButton from "./components/wkt-button";
import {
  time_now,
  local_date_obj,
  LoadingIndicator,
  check_frozen,
} from "./utils/utils";
import {
  faSync,
  faStar,
  faRunning,
  faGlassCheers,
  faTimesCircle,
} from "@fortawesome/free-solid-svg-icons";
import { workette_filters as w_filter } from "./utils/filters";
import DayBigPicture from "./components/day-big-picture";

class DayViewLeft extends Component {
  state = { date: time_now(), certify_mode: false };

  componentDidMount() {
    this.onChange(time_now());
  }

  onChange = (date) => {
    const today = time_now();
    if (this.props.session.freeze_override)
      this.props.set_freeze_override(false);
    if (date > today) date = today;
    this.props.change_date(date);
    const { workette } = this.props;
    const { items, last_day_loaded } = workette;
    const current = workette.days[date.toISOString().split("T")[0]];
    let cert_mode = false;
    if (date < today && !current) {
      this.props.load_day(date.toISOString().split("T")[0]);
    } else if (!current) {
      this.props.load_latest_day(date.toISOString().split("T")[0]);
      cert_mode = true;
    }
    this.setState({ date, certify_mode: cert_mode });
  };

  componentDidUpdate() {
    this.checkForCertifyMode();
    this.checkIfTodayLoaded();
  }

  checkForCertifyMode = () => {
    const { session, workette } = this.props;
    const { items, last_day_loaded } = workette;
    const current = workette.days[session.cur_date];
    if (this.state.certify_mode && !current && last_day_loaded) {
      this.props.change_date(local_date_obj(last_day_loaded));
      this.props.set_freeze_override(true);
    }
  };

  checkIfTodayLoaded = () => {
    const { session, workette } = this.props;
    const { items, last_day_loaded } = workette;
    const current = workette.days[session.cur_date];
    if (
      this.state.certify_mode &&
      this.state.date.toISOString().split("T")[0] === session.cur_date &&
      current
    ) {
      this.setState({ certify_mode: false });
      return true;
    }
    return false;
  };

  onCarryDayForward = () => {
    const dateStr = local_date_obj(this.props.session.cur_date).toDateString();
    if (window.confirm("Ready to freeze " + dateStr + "?")) {
      this.props.load_day(this.state.date.toISOString().split("T")[0]);
      this.setState({ certify_mode: false });
      this.props.change_date(this.state.date);
      this.props.set_freeze_override(false);
    }
  };

  render() {
    const { session, workette } = this.props;
    const { items, last_day_loaded } = workette;
    const current = workette.days[session.cur_date];

    return (
      <Container fluid className="m-0 p-0">
        <Container className="m-0 p-0 day-calendar">
          <small>
            <Calendar
              className="shadow mb-3"
              value={this.state.date}
              onChange={this.onChange}
            />
          </small>

          {this.state.certify_mode && !this.props.api.is_loading.length && (
            <div className="day-cert-button">
              <WktButton
                className=""
                label={
                  current ? "Certify " + session.cur_date : "Start First Day"
                }
                tooltip="Certify prior day before loading today"
                onClick={this.onCarryDayForward}
              />
            </div>
          )}
        </Container>
        {current && (
          <DeepMITs
            w_id={current}
            label="Knock these out!"
            iconProps={{ icon: faStar, color: "gold" }}
            color="starred"
            items={w_filter.deepMIT()}
          />
        )}

        {current && (
          <DeepMITs
            w_id={current}
            label="Babysit these!"
            iconProps={{ icon: faRunning }}
            color="running"
            items={w_filter.deepRunning()}
          />
        )}
        {current && (
          <DeepMITs
            w_id={current}
            label="Active Rituals!"
            iconProps={{ icon: faSync }}
            color="starred"
            items={w_filter.deepActiveRituals()}
          />
        )}
        <Row>
          <Col md="auto">
            <LoadingIndicator
              is_loading={
                this.props.api.is_loading[this.props.api.is_loading.length - 1]
              }
            />
          </Col>
        </Row>
      </Container>
    );
  }
}

const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
  api: state.api,
});

const left_map_dispatch = (dispatch) => ({
  change_date: (date) => dispatch(session.change_date(date)),
  set_freeze_override: (val) => dispatch(session.set_freeze_override(val)),
  load_day: (date) => dispatch(wact.load_day(date)),
  load_latest_day: (date) => dispatch(wact.load_latest_day(date)),
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
            iconProps={{ icon: faGlassCheers, color: "green" }}
            color="mit-completed"
            items={w_filter.deepCompleted()}
          />
        )}

        {current && (
          <DeepMITs
            w_id={current}
            label="Everything Abandoned!"
            iconProps={{ icon: faTimesCircle }}
            color="mit-abandoned"
            items={w_filter.deepCanceled()}
          />
        )}
        {current && (
          <div>
            <Container fluid className="m-0 p-2 mb-3">
              Reflections of the Day
              <Row>
                <Col className=" p-0">
                  <WktNoteForm key={current} w_id={current} />
                </Col>
              </Row>
            </Container>
            <DayBigPicture w_id={current} />
          </div>
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
