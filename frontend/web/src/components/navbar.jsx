import React, { Component } from "react";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { LoadingIndicator, check_frozen } from "../utils/utils";
import logo from "../logo_notext.png";

class NavBar extends Component {
  render() {
    return (
      <nav
        className="navbar navbar-default navbar-expand-lg navbar-light bg-light border"
        role="navigation"
        style={this.props.style}
      >
        <Link className="navbar-brand" to="/">
          <img src={logo} height="35px"></img>
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          {!this.props.session.logged_in && (
            <React.Fragment>
              <ul className="nav navbar-nav  ml-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    Login
                  </Link>
                </li>
                {/* <li className="nav-item">
                  <Link className="nav-link" to="/register">
                    Register
                  </Link>
                </li> */}
              </ul>
            </React.Fragment>
          )}
          {this.props.session.logged_in && (
            <React.Fragment>
              <ul className="nav navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/Day">
                    Day
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/reflect">
                    Reflect (early beta)
                  </Link>
                </li>
              </ul>
              <ul className="nav navbar-nav ml-auto">
                <li className="nav-item">
                  {/* <LoadingIndicator
                    is_loading={
                      this.props.api.is_loading[
                      this.props.api.is_loading.length - 1
                      ]
                    }
                  /> */}
                  {check_frozen(this.props.session) && (
                    <center>
                      <div className="badge badge-primary mr-1">
                        Past Frozen
                      </div>
                    </center>
                  )}
                </li>
              </ul>
              <ul className="nav navbar-nav ml-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/help">
                    Help
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/logout">
                    Logout
                  </Link>
                </li>
              </ul>
            </React.Fragment>
          )}
        </div>
      </nav>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  session: state.session,
  api: state.api,
});

export default connect(map_state)(NavBar);
