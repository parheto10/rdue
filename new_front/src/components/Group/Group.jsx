/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useReducer } from "react";
import { Group246 } from "../Group246";
import "./style.css";

export const Group = ({ property1, className, group = "/img/group-234-2.png" }) => {
  const [state, dispatch] = useReducer(reducer, {
    property1: property1 || "default",
  });

  return (
    <div className={`group ${state.property1} ${className}`}>
      {state.property1 === "default" && (
        <div
          className="overlap-group-wrapper"
          onClick={() => {
            dispatch("click");
          }}
        >
          <div className="overlap-group">
            <div className="rectangle" />
            <img className="img" alt="Group" src={group} />
          </div>
        </div>
      )}

      {state.property1 === "variant-2" && (
        <>
          <div
            className="div"
            onClick={() => {
              dispatch("click");
            }}
          >
            <div className="overlap-group">
              <div className="rectangle" />
              <img className="img" alt="Group" src={group} />
            </div>
          </div>
          <div className="group-wrapper">
            <div className="div-2">
              <div className="div-3">
                <div className="text-wrapper">Agroforêts</div>
                <Group246 className="group-instance" property1="default" />
              </div>
              <div className="div-4">
                <div className="text-wrapper">Forêt classées</div>
                <Group246 className="group-instance" property1="default" />
              </div>
              <div className="div-5">
                <div className="text-wrapper">Parcs et réserves Nationals</div>
                <Group246 className="group-instance" property1="default" />
              </div>
              <div className="div-6">
                <p className="text-wrapper">Zone tampon à 2 km Agrial</p>
                <Group246 className="group-instance" property1="default" />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

function reducer(state, action) {
  if (state.property1 === "default") {
    switch (action) {
      case "click":
        return {
          property1: "variant-2",
        };
    }
  }

  if (state.property1 === "variant-2") {
    switch (action) {
      case "click":
        return {
          property1: "default",
        };
    }
  }

  return state;
}

Group.propTypes = {
  property1: PropTypes.oneOf(["variant-2", "default"]),
  group: PropTypes.string,
};
