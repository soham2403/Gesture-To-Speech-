import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './Pages/Login';
import Homepage from './Pages/Homepage';
import SignupPage from './Pages/SignupPage';
// import VideoCallPage from './Pages/VideocallPage';
// import GestureRecorder from './Pages/TrainCustom';
// import TrainCustom2 from './Pages/TrainCustom2';
import OptionsPage from './Pages/OptionsPage';
import Translate from './Pages/Translate';
import TrainCustom from './Pages/TrainCustom';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Homepage/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/signup' element={<SignupPage/>}/>
        {/* <Route path='/videocall' element={<VideoCallPage/>}/> */}
        <Route path='/traincustom' element={<TrainCustom/>}/>
        {/* <Route path='/traincustom2' element={<TrainCustom2/>}/> */}
        <Route path="/optionPage" element={<OptionsPage/>}/>
        <Route path="/translate" element={<Translate/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
