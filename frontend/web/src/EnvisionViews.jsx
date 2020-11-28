import React, { Component } from "react";
import Workette from "./components/workette";
import "react-calendar/dist/Calendar.css";
import { connect } from "react-redux";
import { workette_actions as wact } from "./store/workette";
import { Row, Col, Tab, Nav } from "react-bootstrap";
import LLCal from "./components/ll-cal";
import {
  LoadingIndicator,
} from "./utils/utils";

class EnvisionViewLeft extends Component {
  componentDidMount() {
    this.load_big_picture();
  }

  componentDidUpdate() {
    if (!this.props.api.is_loading.length) this.load_big_picture();
  }

  load_big_picture = () => {
    const { session, workette } = this.props;
    const { cur_date } = session;
    if (!workette.life[cur_date]) {
      this.props.get_life(cur_date);
    }
    if (!workette.years[cur_date]) {
      this.props.get_year(cur_date);
    }
    if (!workette.months[cur_date]) {
      this.props.get_month(cur_date);
    }
    if (!workette.weeks[cur_date]) {
      this.props.get_week(cur_date);
    }
  }


  render() {
    return (
      <React.Fragment>
        <LLCal hide={true} />
        <Row >
          <Col>
            <Nav variant="pills" className="flex-column">
              <Nav.Item>
                <Nav.Link eventKey="week">Envision Week</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="month">Envision Month</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="year">Envision Year</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="life">Envision Life</Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>

        </Row>
        <Row>
          <Col md="auto">
            <LoadingIndicator
              is_loading={
                this.props.api.is_loading[this.props.api.is_loading.length - 1]
              }
            />
          </Col>
        </Row>
      </React.Fragment>
    );
  }
}

const map_state = (state) => ({
  api: state.api,
  session: state.session,
  workette: state.workette,
});

const left_map_dispatch = (dispatch) => ({
  get_life: (date) => dispatch(wact.get_life(date)),
  get_year: (date) => dispatch(wact.get_year(date)),
  get_month: (date) => dispatch(wact.get_month(date)),
  get_week: (date) => dispatch(wact.get_week(date)),
});

EnvisionViewLeft = connect(map_state, left_map_dispatch)(EnvisionViewLeft);

class EnvisionViewMain extends Component {
  render() {
    const { session, workette } = this.props;
    const { cur_date } = session;
    return (
      <Row>
        <Col>
          <Tab.Content>
            <Tab.Pane eventKey="week">
              Things I must accomplish this <strong>week</strong> are
            {workette.weeks[cur_date] && (
                <Workette w_id={workette.weeks[cur_date]} />
              )}
            </Tab.Pane>
            <Tab.Pane eventKey="month">
              This <strong>month</strong> my key goals are
            {workette.months[cur_date] && (
                <Workette w_id={workette.months[cur_date]} />
              )}
            </Tab.Pane>
            <Tab.Pane eventKey="year">
              By the end of this <strong>year</strong> I want
            {workette.years[cur_date] && (
                <Workette w_id={workette.years[cur_date]} />
              )}
            </Tab.Pane>
            <Tab.Pane eventKey="life">
              <strong>Life's</strong> Mission/Purpose Statement
            {workette.life[cur_date] && (
                <Workette w_id={workette.life[cur_date]} />
              )}
            </Tab.Pane>
          </Tab.Content>
        </Col>
      </Row>
    );
  }
}

EnvisionViewMain = connect(map_state)(EnvisionViewMain);

export { EnvisionViewLeft, EnvisionViewMain };
