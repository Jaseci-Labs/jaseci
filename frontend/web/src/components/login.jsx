import React, { Component } from "react";
import { Input, ServerErrors } from "../utils/utils";
import { connect } from "react-redux";
import { session_actions as session } from "../store/session";
import { workette_actions as wact } from "../store/workette";
import { Redirect } from "react-router-dom";

class LogIn extends Component {
  state = { email: "", pass: "", errors: [] };

  handleSubmit = (e) => {
    const { email, pass } = this.state;
    e.preventDefault();
    //Call server
    this.props.login({ email, pass });

    this.setState({ pass: "" });
  };

  handleChange = (e) => {
    if (e.currentTarget.name === "email") {
      this.setState({ email: e.currentTarget.value });
    } else if (e.currentTarget.name === "password") {
      this.setState({ pass: e.currentTarget.value });
    }
  };

  validate = () => {
    const { email, pass, errors } = this.state;
    errors.length = 0;
    if (email.trim() === "") {
      errors.push("Email required;\n");
    }
    if (pass.trim() === "") {
      errors.push("Password required;\n");
    }
  };

  render() {
    const { email, pass, errors } = this.state;
    return (
      <div className="container-sm">
        {this.props.session.logged_in && <Redirect to="/" />}
        <ServerErrors errors={this.props.session.error} />
        <h1>Login</h1>
        <br />

        <form onSubmit={this.handleSubmit}>
          <Input
            value={email}
            onChange={this.handleChange}
            name="email"
            label="Email address"
            description="Enter a valid email address."
          />
          <Input
            value={pass}
            onChange={this.handleChange}
            name="password"
            type="password"
            label="Password"
            description="Enter your password."
          />

          <button
            disabled={errors.length}
            type="submit"
            className="btn btn-primary"
          >
            Login
          </button>
        </form>
        <br />
      </div>
    );
  }
}

class LogOut extends Component {
  state = {};
  componentDidMount() {
    this.props.logout();
    this.props.wkt_logout();
  }
  render() {
    return <div>{!this.props.session.logged_in && <Redirect to="/" />}</div>;
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  login: ({ email, pass }) => dispatch(session.login({ email, pass })),
  logout: () => dispatch(session.logout()),
  wkt_logout: () => dispatch(wact.logout()),
});

LogIn = connect(map_state, map_dispatch)(LogIn);
LogOut = connect(map_state, map_dispatch)(LogOut);

export { LogIn, LogOut };
