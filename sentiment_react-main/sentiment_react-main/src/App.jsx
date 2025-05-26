import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import SubmitFeedback from './components/SubmitFeedback';
import ViewFeedback from "./components/viewfeedback.jsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<SubmitFeedback />} />
                <Route path="/feedback" element={<ViewFeedback />} />
            </Routes>
        </Router>
    );
}

export default App;
