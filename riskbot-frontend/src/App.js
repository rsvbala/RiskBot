
import React, {useEffect} from 'react';
import Widget from 'rasa-webchat';

import riskBotIcon from './riskbot-icon.png';
import askBot from './askBot.png';

import './App.css';

function App() {

  useEffect(() => {
    localStorage.clear();
  }, []);

  return (
    <div className="App">
      <Widget
        initPayload={"/greet"}
        socketUrl={"http://127.0.0.1:5005"}
        socketPath={"/socket.io/"}
        customData={{"language": "en"}}
        title={(<span>RiskBot</span>)}
        subtitle={""}
        connectOn={'open'}
      />
      <div className="container">
        <div className="header">
          <img src={riskBotIcon} />
          <span className='riskBotTitle'>RiskBot</span>
        </div>
        <div className='contentWrapper'>
        <div className="contentContainer">

          <p>Riskbot is a real-time, interactive bot that provides contextual information regarding customer's security footprint.</p>

          <p>Our users are always on the lookout for information about ransomware and other trending vulnerabilities that their systems are being exposed to. This helps them understand the implications of the vulnerability and helps us set the right expectations. Currently, to acquire this information, our users will have to navigate through filters in the platform which takes some time and effort from their end.</p>

          <p>With Riskbot, users can instantly have access to information regarding their security footprint. Users can get real-time response to questions like trending CVEs, number of ransomware, top vulnerabilities etc.</p>

          <p>Riskbot provides a better customer/user experience by giving new customers a way to quickly assess their security footprint without the need for them dive into the intricacies of the platform. Our aim is to ensure great customer experience by means of offering proactive support.</p>
        </div>
          <div className="askContainer" >
            <div className="askQuestions">
              <p>Ask your security related questions</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
