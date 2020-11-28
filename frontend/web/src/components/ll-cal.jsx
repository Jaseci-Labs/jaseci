import React, { Component } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./ll-cal.scss";
import { connect } from "react-redux";
import { session_actions as session } from "../store/session";
import { workette_actions as wact } from "../store/workette";
import { Container, Collapse, Row, Col } from "react-bootstrap";
import WktButton from "./wkt-button";
import {
  time_now,
  local_date_obj,
} from "../utils/utils";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCalendarAlt,
} from "@fortawesome/free-solid-svg-icons";


class LLCal extends Component {
  state = {
    date: time_now(), certify_mode: false,
    self_expand: this.props.hide ? false : true
  };

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
    const { last_day_loaded } = workette;
    const current = workette.days[session.cur_date];
    if (this.state.certify_mode && !current && last_day_loaded) {
      this.props.change_date(local_date_obj(last_day_loaded));
      this.props.set_freeze_override(true);
    }
  };

  checkIfTodayLoaded = () => {
    const { session, workette } = this.props;
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
    const current = workette.days[session.cur_date];

    return (
      <Container className="m-0 p-0 day-calendar">
        <Row className="justify-content-between" onClick={() => {
          this.setState({
            self_expand: !this.state.self_expand,
          });
        }}>
          <Col
            xs="1"
            className="d-flex flex-column m-0 p-0 justify-content-center align-items-center"
          >
            <FontAwesomeIcon icon={faCalendarAlt} color="black" />
          </Col>
          <Col className="m-0 p-0" style={{ cursor: "pointer" }}>Day Selector</Col>
        </Row>
        <Collapse in={this.state.self_expand} unmountOnExit={true}>
          <div>

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
          </div>
        </Collapse>
      </Container>

    );
  }
}

const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
  api: state.api,
});

const map_dispatch = (dispatch) => ({
  change_date: (date) => dispatch(session.change_date(date)),
  set_freeze_override: (val) => dispatch(session.set_freeze_override(val)),
  load_day: (date) => dispatch(wact.load_day(date)),
  load_latest_day: (date) => dispatch(wact.load_latest_day(date)),
});

export default connect(map_state, map_dispatch)(LLCal);

