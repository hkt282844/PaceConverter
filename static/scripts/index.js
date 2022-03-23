import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Track from "./track";
import Splits from "./splits";
  
// ReactDOM.render(<Track />, document.getElementById("react-root"));

ReactDOM.render(
  <Router>
    <Routes>
      <Route path="/" element={<Splits />} />
      <Route path="/splits" element={<Splits />} />
      <Route path="/track" element={<Track />} />
      <Route path="/track/splits" element={<Track />} />
    </Routes>
  </Router>,

  document.getElementById("react-root")
);
