import React, { Component } from "react";
import { connect } from "react-redux";

const LL_VER = process.env.REACT_APP_LL_VERSION;
const inDevMode = () => LL_VER === "development";

const saveDelayTimeout = (id, func) => {
  clearTimeout(id);
  return setTimeout(() => func(), 1000);
};

const time_now = () => new Date(new Date().toLocaleDateString());

const local_date_obj = (date) => {
  const ldate = new Date(date);
  return new Date(ldate.getTime() + ldate.getTimezoneOffset() * 60000);
};

const todays_date = () => time_now().toISOString().split("T")[0];

const is_today = (date) => {
  const dstr = new Date(date).toISOString().split("T")[0];
  return dstr === todays_date();
};

const check_frozen = (session) => {
  return !is_today(session.cur_date) && !session.freeze_override;
};

/* Generalized Input component for text input must provide value and
and onChange for functionality
important props:
  name,
  type,
  label,
  value,
  onChange,
  description,
  extra_class,
*/
const Input = (props) => {
  return (
    <div className="form-group m-0  pb-1 pt-1">
      {props.label && <label htmlFor={props.name}>{props.label}</label>}
      <input
        {...props}
        className={"form-control " + props.extra_class}
        id={props.name}
        aria-describedby="inputdesc"
      />
      <small id="inputdesc" className="form-text text-muted">
        {props.description}
      </small>
    </div>
  );
};

const TextArea = ({
  name,
  type,
  label,
  value,
  rows,
  onChange,
  description,
  extra_class,
}) => {
  return (
    <div className="form-group m-0  pb-1 pt-1">
      {label && <label htmlFor={name}>{label}</label>}
      <textarea
        value={value}
        onChange={onChange}
        name={name}
        type={type}
        rows={rows}
        className={"form-control " + extra_class}
        id={name}
        aria-describedby="inputdesc"
      />
      <small id="inputdesc" className="form-text text-muted">
        {description}
      </small>
    </div>
  );
};

const Select = ({
  name,
  type,
  label,
  value,
  options,
  onChange,
  description,
  extra_class,
}) => {
  return (
    <div className="form-group m-0 pb-1 pt-1">
      {label && <label htmlFor={name}>{label}</label>}
      <select
        value={value}
        onChange={onChange}
        name={name}
        type={type}
        className={"form-control " + extra_class}
        id={name}
        aria-describedby="inputdesc"
      >
        {options.map((i) => (
          <option key={i}>{i}</option>
        ))}
      </select>

      <small id="inputdesc" className="form-text text-muted">
        {description}
      </small>
    </div>
  );
};

const MultiSelect = ({
  name,
  type,
  label,
  value,
  options,
  onChange,
  description,
  extra_class,
}) => {
  return (
    <div className="form-group m-0  pb-1 pt-1">
      {label && <label htmlFor={name}>{label}</label>}
      <select
        multiple
        value={value}
        onChange={onChange}
        name={name}
        type={type}
        className={"form-control " + extra_class}
        id={name}
        aria-describedby="inputdesc"
      >
        {options.map((i) => (
          <option key={i[0]} label={i[1]}>
            {i[0]}
          </option>
        ))}
      </select>

      <small id="inputdesc" className="form-text text-muted">
        {description}
      </small>
    </div>
  );
};

const CheckBox = ({ name, type, label, value, onChange, extra_class }) => {
  return (
    <div className="form-check form-check-inline m-0  pb-1 pt-1 mr-2">
      <input
        checked={value ? true : false}
        onChange={onChange}
        name={name}
        type="checkbox"
        className={"form-check-input " + extra_class}
        id={name}
        aria-describedby="inputdesc"
      />
      <label className="form-check-label" htmlFor={name}>
        {label}
      </label>
    </div>
  );
};

const ServerErrors = ({ errors }) => {
  return (
    <div>
      {((errors.ferror && errors.ferror.length) || errors.messages) && (
        <div className="alert alert-danger">
          <pre>
            <small>
              {errors.ferror && errors.ferror}
              <br />
              {errors.messages && errors.messages}
              &nbsp;
              {errors.response &&
                errors.response.statusText &&
                errors.response.statusText}
              <br />
              {errors.response &&
              errors.response.data &&
              errors.response.data.non_field_errors
                ? errors.response.data.non_field_errors
                : errors.response &&
                  JSON.stringify(errors.response.data, null, 2)}
            </small>
          </pre>
        </div>
      )}
    </div>
  );
};

const DEVBTN = ({ func, name }) => {
  return (
    <button className="btn btn-primary" onClick={func}>
      {name}
    </button>
  );
};

const LoadingIndicator = ({ is_loading }) => {
  return (
    <React.Fragment>
      {is_loading && (
        <div>
          &nbsp; &nbsp;
          <div className="spinner-grow spinner-grow-sm" role="status">
            <span className="sr-only">Loading...</span>
          </div>
          &nbsp;
          <small>{is_loading}...</small>
        </div>
      )}
    </React.Fragment>
  );
};

class StatusBar extends Component {
  render() {
    return (
      <footer className="footer border" style={this.props.style}>
        <small>{LL_VER}</small>
        <LoadingIndicator
          is_loading={
            this.props.api.is_loading[this.props.api.is_loading.length - 1]
          }
        />
      </footer>
    );
  }
}

//Connect this component to store.session
const StatusBar_map_state = (state) => ({
  api: state.api,
});

StatusBar = connect(StatusBar_map_state)(StatusBar);

function move_arr_item(arr, old_index, new_index) {
  while (old_index < 0) {
    old_index += arr.length;
  }
  while (new_index < 0) {
    new_index += arr.length;
  }
  if (new_index >= arr.length) {
    let k = new_index - arr.length;
    while (k-- + 1) {
      arr.push(undefined);
    }
  }
  arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
  return arr;
}

const wtype_options = ["workette", "link", "note", "workset"];

//Helper to keep sorting in workette lists
function apply_ordering(order, arr) {
  if (Array.isArray(order))
    order
      .filter((el) => arr.includes(el))
      .map((i, idx) => (arr = move_arr_item(arr, arr.indexOf(i), idx)));
  return arr;
}

function validURL(str) {
  var pattern = new RegExp(
    "^(https?:\\/\\/)?" + // protocol
      "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
      "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
      "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
      "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
      "(\\#[-a-z\\d_]*)?$",
    "i"
  ); // fragment locator
  return !!pattern.test(str);
}

export {
  inDevMode,
  time_now,
  local_date_obj,
  todays_date,
  is_today,
  check_frozen,
  saveDelayTimeout,
  Input,
  TextArea,
  Select,
  MultiSelect,
  CheckBox,
  ServerErrors,
  LoadingIndicator,
  DEVBTN,
  StatusBar,
  move_arr_item,
  wtype_options,
  apply_ordering,
  validURL,
};
