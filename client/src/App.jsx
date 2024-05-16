import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import React from "react";


function App() {
  return (
    <BrowserRouter>
      <div className="flex-1 overflow-auto">
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
